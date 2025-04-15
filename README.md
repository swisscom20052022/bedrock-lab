# Bedrock Client

This project contains a Python script for interacting with Amazon Bedrock, a fully managed service that makes foundation models from leading AI companies accessible via an API.

## Requirements

To run this script, you need Python 3.6 or later and the following Python packages:

- boto3
- python-dotenv
- json (part of Python standard library)
- logging (part of Python standard library)

You can install the required packages using the provided `requirements.txt` file:

```
pip install -r requirements.txt
```

## Configuration

1. Copy the `.env.example` file to a new file named `.env`:

   ```
   cp .env.example .env
   ```

2. Open the `.env` file and replace the placeholder values with your specific AWS profile name, region, and the Bedrock model ID you want to use:

   ```
   AWS_PROFILE_NAME=your_aws_profile_name
   AWS_REGION_NAME=your_aws_region
   BEDROCK_MODEL_ID=your_bedrock_model_id
   ```

   Note: The `.env` file is ignored by git to keep your credentials secure.

## AWS Configuration

Make sure you have AWS credentials configured with the necessary permissions to access Amazon Bedrock. You can set up your credentials using the AWS CLI or by setting environment variables. The script will use the profile specified in the `.env` file.

## Usage

1. Ensure you have the required packages installed and AWS credentials configured.
2. Run the script using Python with the following options:

   a. To invoke a model with a custom prompt:
   ```
   python bedrock_client.py invoke "Your custom prompt here" [optional_model_id]
   ```
   This will generate a response based on your prompt and display:
   - The generated text
   - Token count (input and output)
   - Context window usage
   - Estimated API cost

   b. To list available models:
   ```
   python bedrock_client.py list
   ```
   This will display all available foundation models in Amazon Bedrock, including their IDs and names.

   c. To use the default prompt:
   ```
   python bedrock_client.py
   ```
   This will use the default prompt "What's the capital of France?" and display the same information as option (a).

## Output

When invoking a model, the script will display:

1. The input prompt
2. The generated text from the model
3. Usage statistics:
   - Tokens In: Number of tokens in the input prompt
   - Tokens Out: Number of tokens in the generated response
   - Context Window: Total tokens used (in + out) out of the maximum 200,000
   - API Cost: Estimated cost of the API call in USD

## API Cost Calculation

The script includes an estimated API cost calculation based on token usage. This calculation uses a predefined pricing dictionary for different models. Please note:

1. The pricing is an approximation and may not reflect the exact current pricing from AWS.
2. The pricing information is stored in a dictionary within the `calculate_cost` method of the `BedrockClient` class.
3. To get the most accurate pricing:
   - Regularly update the pricing information in the `calculate_cost` method.
   - Consider implementing a method to fetch real-time pricing from AWS.

Current pricing used in the script (per 1000 tokens):

- anthropic.claude-v2: $0.01102 (input), $0.03268 (output)
- anthropic.claude-v1: $0.01102 (input), $0.03268 (output)
- anthropic.claude-instant-v1: $0.00163 (input), $0.00551 (output)
- ai21.j2-mid-v1: $0.01 (input), $0.02 (output)
- ai21.j2-ultra-v1: $0.03 (input), $0.06 (output)

For unlisted models, a default pricing of $0.01 (input) and $0.03 (output) per 1000 tokens is used.

## Script Overview

The `bedrock_client.py` script includes the following main components:

- `BedrockClient` class: Handles interactions with Amazon Bedrock, including listing models, getting model details, and invoking models.
- `main()` function: Demonstrates the usage of the `BedrockClient` class.

For more details on the available methods and their usage, please refer to the comments in the `bedrock_client.py` file.

## Note

This script is configured to use a specific AWS profile and region. Make sure to update these values in the `BedrockClient` initialization if needed.
