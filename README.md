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
2. Run the script using Python:

You can now use the script as follows:

To use a custom prompt:

```
python bedrock_client.py "Your custom prompt here"
```

To use the default prompt:

```
python bedrock_client.py
```

The script will invoke the Bedrock model with the provided prompt (or the default prompt if none is given), display the generated text, and then list the available models.

## Script Overview

The `bedrock_client.py` script includes the following main components:

- `BedrockClient` class: Handles interactions with Amazon Bedrock, including listing models, getting model details, and invoking models.
- `main()` function: Demonstrates the usage of the `BedrockClient` class.

For more details on the available methods and their usage, please refer to the comments in the `bedrock_client.py` file.

## Note

This script is configured to use a specific AWS profile and region. Make sure to update these values in the `BedrockClient` initialization if needed.
