import json
import random

# Input JSONL file
input_file = "generated_summaries.jsonl"

# Output files
low_file = "low_granularity_repos.json"
medium_file = "medium_granularity_repos.json"
high_file = "high_granularity_repos.json"

# Buckets
low, medium, high = [], [], []

# Step 1: Load JSONL
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            data = json.loads(line)
            granularity = data.get("Granularity", "").strip().lower()
            if granularity == "low":
                low.append(data)
            elif granularity == "medium":
                medium.append(data)
            elif granularity == "high":
                high.append(data)

# Step 2: Randomly sample 10 from each (or all if <10 available)
low_sample = random.sample(low, min(10, len(low)))
medium_sample = random.sample(medium, min(10, len(medium)))
high_sample = random.sample(high, min(10, len(high)))

# Step 3: Write to separate JSON files (as proper JSON arrays)
def write_json(filename, data_list):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data_list, f, indent=4, ensure_ascii=False)

write_json(low_file, low_sample)
write_json(medium_file, medium_sample)
write_json(high_file, high_sample)

print(f"✅ Saved {len(low_sample)} low, {len(medium_sample)} medium, {len(high_sample)} high repositories.")
print(f"Files created: {low_file}, {medium_file}, {high_file}")
