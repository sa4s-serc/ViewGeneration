import json
import re
import csv

def extract_repo_url(link):
    match = re.match(r"(https://github\.com/[^/]+/[^/]+)", link)
    return match.group(1) + "/" if match else link

# File paths
jsonl_path = "summaries.jsonl"
csv_path = "filtered_output.csv"
output_path = "summaries_enriched.jsonl"

# Build a lookup dictionary from CSV using Image URL
csv_data = {}
with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        repo_url = extract_repo_url(row["Image URL"].strip())
        if repo_url:
            csv_data[repo_url] = {
                "Concern": row.get("Concern", "").strip(),
                "Behavior": row.get("Behavior", "").strip(),
                "Repository Name": row.get("Repository Name", "").strip()
            }

# Update JSONL entries with matched Concern and Behavior
with open(jsonl_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
    for line in infile:
        data = json.loads(line)
        repo_url = extract_repo_url(data.get("repo_url", "").strip())

        if repo_url in csv_data:
            data["Concern"] = csv_data[repo_url]["Concern"]
            data["Behavior"] = csv_data[repo_url]["Behavior"]
            data["Repository Name"] = csv_data[repo_url]["Repository Name"]

        outfile.write(json.dumps(data) + '\n')

print("✅ Enrichment complete. Output written to:", output_path)
