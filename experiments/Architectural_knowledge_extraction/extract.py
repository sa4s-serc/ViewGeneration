import json
import csv

max_tokens = 0
total_tokens = 0
count = 0
rows = []

# Read JSONL and extract data
with open('summaries.jsonl', 'r') as file:
    for line in file:
        data = json.loads(line)
        repo_url = data['repo_url']
        token_count = data['summary_token_count']
        rows.append([repo_url, token_count])

        # Statistics
        if token_count > max_tokens:
            max_tokens = token_count
        total_tokens += token_count
        count += 1

# Write to CSV
with open('summaries_token_count.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['repo_url', 'summary_token_count'])  # Header
    writer.writerows(rows)

# Compute average
avg_tokens = total_tokens / count if count else 0
# Output stats
print(f"Maximum summary_token_count: {max_tokens}")
print(f"Average summary_token_count: {avg_tokens:.2f}")
