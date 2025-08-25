import json
from collections import defaultdict

def calculate_average_code_tokens_by_granularity(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Dictionary to store total tokens and counts per granularity
    granularity_stats = defaultdict(lambda: {"total_tokens": 0, "count": 0})

    for entry in data:
        granularity = entry.get("Granularity")
        code_tokens = entry.get("code_tokens", 0)

        if granularity:
            granularity_stats[granularity]["total_tokens"] += code_tokens
            granularity_stats[granularity]["count"] += 1

    # Calculate averages
    averages = {
        granularity: stats["total_tokens"] / stats["count"]
        for granularity, stats in granularity_stats.items()
    }

    return averages

if __name__ == "__main__":
    averages = calculate_average_code_tokens_by_granularity('examples.json')
    for granularity, avg in averages.items():
        print(f"Granularity: {granularity}, Average code_tokens: {avg:.2f}")



#output : Granularity: high, Average code_tokens: 292.00
# Granularity: medium, Average code_tokens: 582.00