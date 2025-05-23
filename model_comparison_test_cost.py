import sys
from bedrock_client import BedrockClient
from tabulate import tabulate

def run_cost_comparison_tests():
    bedrock = BedrockClient()

    test_prompts = [
        ("Short", "Translate 'Hello, how are you?' into French."),
        ("Medium", "Summarize the following paragraph:\n\nArtificial intelligence (AI) is intelligence demonstrated by machines, as opposed to natural intelligence displayed by animals including humans. AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals."),
        ("Long", "Write a detailed essay about the impact of AI on cybersecurity in 2025. Include at least three main points and provide examples for each."),
        ("Very Long", "Given this legal contract (simulated 5000 words):\n\n" + "Lorem ipsum " * 500)
    ]

    models = [
        "anthropic.claude-3-5-sonnet-20240620-v1:0",
        "anthropic.claude-3-haiku-20240307-v1:0"
    ]

    results = []
    total_costs = {"sonnet": 0, "haiku": 0}

    for prompt_type, prompt in test_prompts:
        row = [prompt_type]
        for model in models:
            print(f"Testing {model} with prompt type: {prompt_type}")
            response, usage_stats = bedrock.invoke_bedrock_model(prompt, model_id=model)
            model_name = "sonnet" if "sonnet" in model else "haiku"
            print(f"\n{model_name.capitalize()} Input:")
            print(prompt)
            print(f"\n{model_name.capitalize()} Output:")
            print(response)
            row.extend([
                usage_stats['tokens_in'],
                usage_stats['tokens_out'],
                usage_stats['api_cost']
            ])
            total_costs[model_name] += usage_stats['api_cost']
        results.append(row)

    headers = ['Prompt Type'] + sum([[f'{model.split("-")[2] if "haiku" in model else "sonnet"} In', f'{model.split("-")[2] if "haiku" in model else "sonnet"} Out', f'{model.split("-")[2] if "haiku" in model else "sonnet"} Cost'] for model in models], [])
    print("\nComparison Table:")
    print(tabulate(results, headers=headers, tablefmt="grid"))

    # Add total costs to the results
    results.append(["Total Cost", "", "", total_costs["sonnet"], "", "", total_costs["haiku"]])
    print("\nTotal Costs:")
    print(tabulate([results[-1]], headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    run_cost_comparison_tests()
