import csv
import json
import os
import statistics

# Paths
low_granularity_file = "../../../../Architectural_knowledge_extraction/UML.jsonl"
ratings_csv = "ratings_summary.csv"
output_csv = "low_granularity_ratings.csv"

# Step 1: Load low-granularity repo names
low_granularity_repos = set()
with open(low_granularity_file, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            data = json.loads(line)
            repo_name = data.get("Repository Name", "").strip()
            if repo_name:
                repo_name_clean = repo_name.replace("/", "_").replace("\\", "_").rstrip("_")
                low_granularity_repos.add(repo_name_clean)

# Step 2: Filter ratings.csv
filtered_rows = []
ratings = []

with open(ratings_csv, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        filename_base = os.path.splitext(row["Filename"])[0]
        repo_candidate = filename_base.replace("_comparison", "")

        if repo_candidate in low_granularity_repos:
            filtered_rows.append(row)
            try:
                ratings.append(float(row["Rating"]))
            except ValueError:
                pass  # Skip invalid ratings

# Step 3: Save to new CSV
if filtered_rows:
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Filename", "Rating"])
        writer.writeheader()
        writer.writerows(filtered_rows)

    print(f"✅ Saved {len(filtered_rows)} low-granularity entries to {output_csv}")

    # Step 4: Calculate statistics
    if ratings:
        mean_val = statistics.mean(ratings)
        median_val = statistics.median(ratings)
        variance_val = statistics.variance(ratings) if len(ratings) > 1 else 0.0
        std_dev = statistics.stdev(ratings) if len(ratings) > 1 else 0.0

        print("\n📊 Statistics for low-granularity ratings:")
        print(f"Mean:     {mean_val:.4f}")
        print(f"Median:   {median_val:.4f}")
        print(f"Variance: {variance_val:.4f}")
        print(f"Std Dev:  {std_dev:.4f}")
    else:
        print("⚠️ No valid ratings found for statistics.")

else:
    print("⚠️ No matching low-granularity entries found.")

# Mean:     6.4615
# Median:   7.0000
# Variance: 2.4185
# Std Dev:  1.5551


#UML
# Mean:     6.5000
# Median:   7.0000
# Variance: 3.0385
# Std Dev:  1.7431