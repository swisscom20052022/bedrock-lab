import boto3
import json
import logging
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BedrockClient:
    def __init__(self, profile_name='954753067569', region_name='eu-central-2'):
        session = boto3.Session(profile_name=profile_name, region_name=region_name)
        self.bedrock_client = session.client(service_name="bedrock")
        self.bedrock_runtime = session.client(service_name="bedrock-runtime")

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

    def invoke_bedrock_model(self, prompt, model_id="anthropic.claude-3-5-sonnet-20240620-v1:0", max_tokens=8192, temperature=0.5):
        """
        Invokes an Amazon Bedrock model and returns the generated text.

        :param prompt: The input prompt for the model
        :param model_id: The ID of the model to use (default: anthropic.claude-3-5-sonnet-20240620-v1:0)
        :param max_tokens: Maximum number of tokens to generate (default: 8192)
        :param temperature: Temperature for text generation (default: 0.5)
        :return: Generated text from the model
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

            response = self.bedrock_runtime.invoke_model(
                body=json.dumps(payload),
                modelId=model_id,
                contentType="application/json",
                accept="application/json"
            )

            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text'].strip()
        except ClientError as e:
            logger.error(f"An error occurred: {e}")
            return None

def main():
    bedrock = BedrockClient()

    # List available models
    print("Listing available models:")
    try:
        models = bedrock.list_foundation_models()
        for model in models:
            print(f"- {model['modelId']}: {model['modelName']}")
    except Exception as e:
        print(f"Error listing models: {e}")

    # Invoke the model
    print("\nInvoking model:")
    prompt = "\n\nHuman: What's the capital of France?\n\nAssistant:"
    try:
        result = bedrock.invoke_bedrock_model(prompt)
        if result:
            print("Generated text:", result)
        else:
            print("No text generated.")
    except Exception as e:
        print(f"Error invoking model: {e}")

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
