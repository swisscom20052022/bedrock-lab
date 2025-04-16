import time
from bedrock_client import BedrockClient, invoke_model

def run_model_comparison(prompts, models):
    bedrock = BedrockClient()
    results = {}

    for model in models:
        results[model] = []
        for prompt in prompts:
            print(f"\nTesting model: {model}")
            print(f"Prompt: {prompt}")
            
            start_time = time.time()
            result, usage_stats = bedrock.invoke_bedrock_model(prompt, model_id=model)
            end_time = time.time()
            
            if result and usage_stats:
                total_time = end_time - start_time
                tokens_per_second = (usage_stats['tokens_in'] + usage_stats['tokens_out']) / total_time
                
                results[model].append({
                    'prompt': prompt,
                    'result': result,
                    'tokens_in': usage_stats['tokens_in'],
                    'tokens_out': usage_stats['tokens_out'],
                    'total_tokens': usage_stats['tokens_in'] + usage_stats['tokens_out'],
                    'api_cost': usage_stats['api_cost'],
                    'inference_time': total_time,
                    'tokens_per_second': tokens_per_second
                })
                
                print(f"Generated text: {result[:100]}...")  # Print first 100 characters
                print(f"Tokens In: {usage_stats['tokens_in']}")
                print(f"Tokens Out: {usage_stats['tokens_out']}")
                print(f"Total Tokens: {usage_stats['tokens_in'] + usage_stats['tokens_out']}")
                print(f"API Cost: ${usage_stats['api_cost']:.6f}")
                print(f"Inference Time: {total_time:.2f} seconds")
                print(f"Tokens per Second: {tokens_per_second:.2f}")
            else:
                print("Error: No result or usage stats available.")

    return results

def compare_results(results):
    models = list(results.keys())
    metrics = ['tokens_in', 'tokens_out', 'total_tokens', 'api_cost', 'inference_time', 'tokens_per_second']
    
    print("\n=== Model Comparison ===")
    for metric in metrics:
        print(f"\n{metric.replace('_', ' ').title()}:")
        for model in models:
            values = [r[metric] for r in results[model]]
            avg_value = sum(values) / len(values)
            print(f"{model}: {avg_value:.2f}")

if __name__ == "__main__":
    test_prompts = [
        "Explain the concept of quantum entanglement in simple terms.",
        "Write a short story about a robot learning to paint.",
        "Describe the process of photosynthesis step by step.",
        "Compare and contrast the Renaissance and the Enlightenment periods.",
        "Provide a brief history of the Internet and its impact on society."
    ]
    
    models_to_test = [
        "anthropic.claude-3-haiku-20240307-v1:0",
        "anthropic.claude-3-5-sonnet-20240620-v1:0"
    ]
    
    results = run_model_comparison(test_prompts, models_to_test)
    compare_results(results)
