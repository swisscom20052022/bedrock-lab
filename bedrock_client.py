import boto3
import json
import logging
import os
import sys
import time
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

    def calculate_cost(self, tokens_in, tokens_out, model_id):
        # Fetch actual pricing information from AWS API or use a predefined pricing dictionary
        # This is a placeholder. Replace with actual API call or up-to-date pricing information
        pricing = {
            "anthropic.claude-v2": {"input": 0.00001102, "output": 0.00003268},
            "anthropic.claude-v1": {"input": 0.00001102, "output": 0.00003268},
            "anthropic.claude-instant-v1": {"input": 0.00000163, "output": 0.00000551},
            "ai21.j2-mid-v1": {"input": 0.00001, "output": 0.00002},
            "ai21.j2-ultra-v1": {"input": 0.00003, "output": 0.00006},
        }
        
        model_pricing = pricing.get(model_id, {"input": 0.00001, "output": 0.00003})  # Default pricing if model not found
        return (tokens_in * model_pricing["input"] + tokens_out * model_pricing["output"]) / 1000

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
        :param model_id: The ID of the model to use (default: anthropic.claude-v2)
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

            model_id = model_id or os.getenv('BEDROCK_MODEL_ID', 'anthropic.claude-v2')
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
            self.api_cost = self.calculate_cost(self.tokens_in, self.tokens_out, model_id)

            return generated_text, {
                "tokens_in": self.tokens_in,
                "tokens_out": self.tokens_out,
                "context_window": self.context_window,
                "api_cost": self.api_cost
            }
        except ClientError as e:
            logger.error(f"An error occurred: {e}")
            return None, None

def invoke_model(bedrock, prompt, model_id=None):
    print(f"\nInvoking model with prompt: {prompt}")
    try:
        start_time = time.time()
        result, usage_stats = bedrock.invoke_bedrock_model(prompt, model_id)
        end_time = time.time()
        total_time = end_time - start_time
        
        if result:
            print("Generated text:", result)
            print("\nUsage Statistics:")
            print(f"Tokens In: {usage_stats['tokens_in']}")
            print(f"Tokens Out: {usage_stats['tokens_out']}")
            print(f"Total Tokens: {usage_stats['tokens_in'] + usage_stats['tokens_out']}")
            print(f"Context Window: {usage_stats['context_window']} / 200,000")
            print(f"API Cost: ${usage_stats['api_cost']:.6f}")
            print("\nSpeed Insights:")
            print(f"Total Inference Time: {total_time:.2f} seconds")
            print(f"Tokens per Second: {(usage_stats['tokens_in'] + usage_stats['tokens_out']) / total_time:.2f}")
            print(f"Input Tokens per Second: {usage_stats['tokens_in'] / total_time:.2f}")
            print(f"Output Tokens per Second: {usage_stats['tokens_out'] / total_time:.2f}")
        else:
            print("No text generated.")
    except Exception as e:
        print(f"Error invoking model: {e}")

def list_models(bedrock):
    print("\nListing available models:")
    try:
        models = bedrock.list_foundation_models()
        for model in models:
            print(f"- {model['modelId']}: {model['modelName']}")
    except Exception as e:
        print(f"Error listing models: {e}")

def main():
    """
    Main function to demonstrate the usage of BedrockClient.

    Usage:
    1. To invoke a model with a custom prompt:
       python bedrock_client.py invoke "Your custom prompt here" [optional_model_id]

    2. To list available models:
       python bedrock_client.py list

    3. To use the default prompt:
       python bedrock_client.py

    The script will perform the specified action based on the command-line arguments.
    """
    bedrock = BedrockClient()

    if len(sys.argv) > 1:
        if sys.argv[1] == "invoke":
            prompt = sys.argv[2] if len(sys.argv) > 2 else "What's the capital of France?"
            model_id = sys.argv[3] if len(sys.argv) > 3 else None
            invoke_model(bedrock, prompt, model_id)
        elif sys.argv[1] == "list":
            list_models(bedrock)
        else:
            print("Invalid command. Use 'invoke' or 'list'.")
    else:
        # Default behavior: invoke with default prompt
        invoke_model(bedrock, "What's the capital of France?")

if __name__ == "__main__":
    main()
