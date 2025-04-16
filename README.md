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
   - Total Tokens: Sum of input and output tokens
   - Context Window: Total tokens used (in + out) out of the maximum 200,000
   - API Cost: Estimated cost of the API call in USD
4. Speed Insights:
   - Total Inference Time: Time taken for the entire process in seconds
   - Tokens per Second: Overall processing speed (input + output)
   - Input Tokens per Second: Speed of processing input tokens
   - Output Tokens per Second: Speed of generating output tokens

## Available Models

As of the last update, the following models are available:

- amazon.titan-embed-text-v2:0:8k: Titan Text Embeddings V2
- amazon.titan-embed-text-v2:0: Titan Text Embeddings V2
- anthropic.claude-3-haiku-20240307-v1:0: Claude 3 Haiku
- anthropic.claude-3-5-sonnet-20240620-v1:0: Claude 3.5 Sonnet

To get the most up-to-date list of available models, run:

```
python bedrock_client.py list
```

## Model Comparison

| Model | Input Token Price (per 1K) | Output Token Price (per 1K) | Input Token Price (per 1M) | Output Token Price (per 1M) | Context Window | Key Features |
|-------|----------------------------|----------------------------|---------------------------|---------------------------|----------------|--------------|
| Claude 3 Haiku | $0.00025 | $0.00125 | $0.25 | $1.25 | 200k tokens | • Fastest and most compact model<br>• Optimized for low-latency, high-throughput use cases<br>• Ideal for cost-sensitive workloads |
| Claude 3.5 Sonnet | $0.003 (1200%) | $0.015 (1200%) | $3.00 (1200%) | $15.00 (1200%) | 200k tokens | • Anthropic's most intelligent model (as of April 2025)<br>• Delivers Claude 3 Opus-level intelligence at one-fifth the cost<br>• Ideal for complex, context-sensitive applications<br>• Supports batch inference and latency-optimized options |

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

## Model Comparison Results

A comparison test was run between Claude 3 Haiku (anthropic.claude-3-haiku-20240307-v1:0) and Claude 3.5 Sonnet (anthropic.claude-3-5-sonnet-20240620-v1:0). Here are the key findings:

1. Tokens In: Both models used an average of 9.60 input tokens.

2. Tokens Out:
   - Claude 3 Haiku: 313.60 tokens
   - Claude 3.5 Sonnet: 331.60 tokens
   Claude 3.5 Sonnet generated slightly more output tokens on average.

3. Total Tokens:
   - Claude 3 Haiku: 323.20 tokens
   - Claude 3.5 Sonnet: 341.20 tokens

4. API Cost: Negligible difference for both models in this test.

5. Inference Time:
   - Claude 3 Haiku: 5.75 seconds
   - Claude 3.5 Sonnet: 12.48 seconds
   Claude 3 Haiku is significantly faster, taking less than half the time of Claude 3.5 Sonnet.

6. Tokens Per Second:
   - Claude 3 Haiku: 63.05 tokens/second
   - Claude 3.5 Sonnet: 27.61 tokens/second
   Claude 3 Haiku processes tokens more than twice as fast as Claude 3.5 Sonnet.

Key Findings:
1. Speed: Claude 3 Haiku is considerably faster than Claude 3.5 Sonnet.
2. Output Length: Claude 3.5 Sonnet tends to produce slightly longer responses on average.
3. Cost: No significant difference in API cost for short prompts.

Recommendations:
- Use Claude 3 Haiku for tasks requiring quick responses or real-time interactions.
- Consider Claude 3.5 Sonnet for tasks that may benefit from more detailed responses.
- For cost-sensitive applications with short prompts, either model is suitable.
- Further testing with longer, more complex prompts is recommended to evaluate response quality and accuracy.

## Detailed Cost Comparison Results

A more detailed cost comparison test was conducted between Claude 3 Haiku and Claude 3.5 Sonnet models using prompts of varying lengths. Here are the results:

```
+---------------+------------+-------------+--------------+--------+---------+----------+
| Prompt Type   |   haiku In |   haiku Out |   haiku Cost |   5 In |   5 Out |   5 Cost |
+===============+============+=============+==============+========+=========+==========+
| Short         |          7 |          14 |    1.925e-05 |      7 |      80 | 0.001221 |
+---------------+------------+-------------+--------------+--------+---------+----------+
| Medium        |         55 |          83 |    0.0001175 |     55 |      43 | 0.00081  |
+---------------+------------+-------------+--------------+--------+---------+----------+
| Long          |         24 |         476 |    0.000601  |     24 |     742 | 0.011202 |
+---------------+------------+-------------+--------------+--------+---------+----------+
| Very Long     |       1007 |         131 |    0.0004155 |   1007 |     147 | 0.005226 |
+---------------+------------+-------------+--------------+--------+---------+----------+
```

### Analysis of Results

1. Short Prompts:
   - Haiku: 7 tokens in, 14 tokens out, cost $0.00001925
   - Sonnet: 7 tokens in, 80 tokens out, cost $0.001221
   - Sonnet is about 63 times more expensive for short prompts.

2. Medium Prompts:
   - Haiku: 55 tokens in, 83 tokens out, cost $0.0001175
   - Sonnet: 55 tokens in, 43 tokens out, cost $0.00081
   - Sonnet is about 6.9 times more expensive for medium prompts.

3. Long Prompts:
   - Haiku: 24 tokens in, 476 tokens out, cost $0.000601
   - Sonnet: 24 tokens in, 742 tokens out, cost $0.011202
   - Sonnet is about 18.6 times more expensive for long prompts.

4. Very Long Prompts:
   - Haiku: 1007 tokens in, 131 tokens out, cost $0.0004155
   - Sonnet: 1007 tokens in, 147 tokens out, cost $0.005226
   - Sonnet is about 12.6 times more expensive for very long prompts.

### Key Observations

1. Claude-3-Sonnet is consistently more expensive across all prompt types.
2. The cost difference is most pronounced for short prompts, where Sonnet is 63 times more expensive.
3. For medium to very long prompts, Sonnet is roughly 7 to 19 times more expensive than Haiku.
4. Sonnet tends to generate more tokens in output for the same input, especially for shorter prompts.

### Recommendations

1. For cost-sensitive applications, especially those dealing with shorter prompts, Claude 3 Haiku is significantly more economical.
2. If the advanced capabilities of Sonnet are not critical for the task, using Haiku could lead to substantial cost savings.
3. For applications requiring more detailed or nuanced responses, the higher cost of Sonnet may be justified by its potentially superior output quality.
4. Consider the specific requirements of your use case when choosing between these models, balancing cost efficiency with output quality and complexity.

This cost comparison provides valuable insights for decision-making when selecting between Claude 3 Haiku and Claude 3.5 Sonnet models. The choice between them should be based on the specific needs of the task, considering factors such as budget constraints, required response quality, and the complexity of the prompts being used.
