# import json
# import re
# import csv

# def extract_repo_url(link):
#     match = re.match(r"(https://github\.com/[^/]+/[^/]+)", link)
#     return match.group(1) + "/" if match else link

# # File paths
# jsonl_path = "summaries.jsonl"
# csv_path = "filtered_output.csv"
# output_path = "summaries_enriched.jsonl"

# # Build a lookup dictionary from CSV using Image URL
# csv_data = {}
# with open(csv_path, newline='', encoding='utf-8') as csvfile:
#     reader = csv.DictReader(csvfile, delimiter=';')
#     for row in reader:
#         repo_url = extract_repo_url(row["Image URL"].strip())
#         if repo_url:
#             csv_data[repo_url] = {
#                 "Concern": row.get("Concern", "").strip(),
#                 "Behavior": row.get("Behavior", "").strip(),
#                 "Repository Name": row.get("Repository Name", "").strip()
#             }

# # Update JSONL entries with matched Concern and Behavior
# with open(jsonl_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
#     for line in infile:
#         data = json.loads(line)
#         repo_url = extract_repo_url(data.get("repo_url", "").strip())

#         if repo_url in csv_data:
#             data["Concern"] = csv_data[repo_url]["Concern"]
#             data["Behavior"] = csv_data[repo_url]["Behavior"]
#             data["Repository Name"] = csv_data[repo_url]["Repository Name"]

#         outfile.write(json.dumps(data) + '\n')

# print("✅ Enrichment complete. Output written to:", output_path)

import json
import csv

# File paths
csv_file = "filtered_output.csv"
jsonl_file = "generated_summaries.jsonl"
output_file = "merged.jsonl"

# Step 1: Load CSV data into a dictionary by Repository Name
csv_data = {}
with open(csv_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')  # You used semicolon-separated CSV
    for row in reader:
        repo_name = row["Repository Name"].strip()
        csv_data[repo_name] = row

# Step 2: Load JSONL file
jsonl_entries = []
with open(jsonl_file, "r", encoding="utf-8") as f:
    for line in f:
        entry = json.loads(line)
        jsonl_entries.append(entry)

# Step 3: Merge CSV data into JSONL entries
merged_entries = []
for entry in jsonl_entries:
    repo_name = entry.get("Repository Name", "").strip()
    if repo_name in csv_data:
        # Add all CSV fields into the JSONL entry
        entry.update(csv_data[repo_name])
    else:
        print(f"Warning: No CSV match for repo '{repo_name}'")
    merged_entries.append(entry)

# Step 4: Write merged entries to new JSONL file
with open(output_file, "w", encoding="utf-8") as f:
    for entry in merged_entries:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

print(f"Merged {len(merged_entries)} entries to {output_file}")

