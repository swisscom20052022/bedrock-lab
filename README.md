# Bedrock Client

This project contains a Python script for interacting with Amazon Bedrock, a fully managed service that makes foundation models from leading AI companies accessible via an API.

## Requirements

To run this script, you need Python 3.6 or later and the following Python packages:

- boto3
- json (part of Python standard library)
- logging (part of Python standard library)

You can install the required package using pip:

```
pip install boto3
```

## AWS Configuration

Make sure you have AWS credentials configured with the necessary permissions to access Amazon Bedrock. You can set up your credentials using the AWS CLI or by setting environment variables.

## Usage

1. Ensure you have the required packages installed and AWS credentials configured.
2. Run the script using Python:

```
python bedrock_client.py
```

The script will list available foundation models and attempt to invoke a model with a sample prompt.

## Script Overview

The `bedrock_client.py` script includes the following main components:

- `BedrockClient` class: Handles interactions with Amazon Bedrock, including listing models, getting model details, and invoking models.
- `main()` function: Demonstrates the usage of the `BedrockClient` class.

For more details on the available methods and their usage, please refer to the comments in the `bedrock_client.py` file.

## Note

This script is configured to use a specific AWS profile and region. Make sure to update these values in the `BedrockClient` initialization if needed.
