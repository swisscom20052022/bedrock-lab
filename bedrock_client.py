import boto3
import json
import logging
import os
import sys
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BedrockClient:
    def __init__(self):
        profile_name = os.getenv('AWS_PROFILE_NAME')
        region_name = os.getenv('AWS_REGION_NAME')
        session = boto3.Session(profile_name=profile_name, region_name=region_name)
        self.bedrock_client = session.client(service_name="bedrock")
        self.bedrock_runtime = session.client(service_name="bedrock-runtime")
        self.tokens_in = 0
        self.tokens_out = 0
        self.context_window = 0
        self.api_cost = 0

    def calculate_tokens(self, text):
        # This is a simple approximation. For accurate token count, use the model's tokenizer.
        return len(text.split())

    def calculate_cost(self, tokens_in, tokens_out):
        # This is an example cost calculation. Adjust based on actual AWS Bedrock pricing.
        return (tokens_in * 0.00001 + tokens_out * 0.00003) / 1000

    def list_foundation_models(self):
        """
        List the available Amazon Bedrock foundation models.

        :return: The list of available bedrock foundation models.
        """
        try:
            response = self.bedrock_client.list_foundation_models()
            models = response["modelSummaries"]
            logger.info("Got %s foundation models.", len(models))
            return models
        except ClientError:
            logger.error("Couldn't list foundation models.")
            raise

    def get_foundation_model(self, model_identifier):
        """
        Get details about an Amazon Bedrock foundation model.

        :param model_identifier: The identifier of the model to get details for.
        :return: The foundation model's details.
        """
        try:
            response = self.bedrock_client.get_foundation_model(modelIdentifier=model_identifier)
            return response["modelDetails"]
        except ClientError:
            logger.error(f"Couldn't get foundation model details for {model_identifier}")
            raise

    def invoke_bedrock_model(self, prompt, model_id=None, max_tokens=8192, temperature=0.5):
        """
        Invokes an Amazon Bedrock model and returns the generated text along with usage statistics.

        :param prompt: The input prompt for the model
        :param model_id: The ID of the model to use (default: anthropic.claude-3-5-sonnet-20240620-v1:0)
        :param max_tokens: Maximum number of tokens to generate (default: 8192)
        :param temperature: Temperature for text generation (default: 0.5)
        :return: Tuple containing generated text and usage statistics
        """
        try:
            payload = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": temperature
            }

            model_id = model_id or os.getenv('BEDROCK_MODEL_ID')
            response = self.bedrock_runtime.invoke_model(
                body=json.dumps(payload),
                modelId=model_id,
                contentType="application/json",
                accept="application/json"
            )

            response_body = json.loads(response['body'].read())
            generated_text = response_body['content'][0]['text'].strip()

            self.tokens_in = self.calculate_tokens(prompt)
            self.tokens_out = self.calculate_tokens(generated_text)
            self.context_window = self.tokens_in + self.tokens_out
            self.api_cost = self.calculate_cost(self.tokens_in, self.tokens_out)

            return generated_text, {
                "tokens_in": self.tokens_in,
                "tokens_out": self.tokens_out,
                "context_window": self.context_window,
                "api_cost": self.api_cost
            }
        except ClientError as e:
            logger.error(f"An error occurred: {e}")
            return None, None

def main():
    """
    Main function to demonstrate the usage of BedrockClient.

    Usage:
    1. To use a custom prompt:
       python bedrock_client.py "Your custom prompt here"

    2. To use the default prompt:
       python bedrock_client.py

    The script will invoke the Bedrock model with the provided prompt
    (or the default prompt if none is given), display the generated text,
    and then list the available models.
    """
    bedrock = BedrockClient()

    # Get prompt from command line argument or use default
    prompt = sys.argv[1] if len(sys.argv) > 1 else "What's the capital of France?"
    
    # Invoke the model
    print("\nInvoking model with prompt:", prompt)
    try:
        result, usage_stats = bedrock.invoke_bedrock_model(prompt)
        if result:
            print("Generated text:", result)
            print("\nUsage Statistics:")
            print(f"Tokens In: {usage_stats['tokens_in']}")
            print(f"Tokens Out: {usage_stats['tokens_out']}")
            print(f"Context Window: {usage_stats['context_window']} / 200,000")
            print(f"API Cost: ${usage_stats['api_cost']:.4f}")
        else:
            print("No text generated.")
    except Exception as e:
        print(f"Error invoking model: {e}")

    # List available models
    print("\nListing available models:")
    try:
        models = bedrock.list_foundation_models()
        for model in models:
            print(f"- {model['modelId']}: {model['modelName']}")
    except Exception as e:
        print(f"Error listing models: {e}")

    # Uncomment this block if you want to get model details
    # try:
    #     model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    #     model_details = bedrock.get_foundation_model(model_id)
    #     print(f"\nDetails for model {model_id}:")
    #     print(json.dumps(model_details, indent=2))
    # except Exception as e:
    #     print(f"Error getting model details: {e}")

if __name__ == "__main__":
    main()
