import os
import json
import csv
import statistics

# Path to your folder
json_folder = "LLM_as_a_Judge_openai_outputs"
csv_filename = "ratings_summary.csv"

# Collect filename and ratings
ratings_data = []

for file in os.listdir(json_folder):
    if file.endswith(".json"):
        file_path = os.path.join(json_folder, file)
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                rating = data.get("comparison", {}).get("Rating", None)
                if rating is not None:
                    ratings_data.append((file, rating))
        except Exception as e:
            print(f"Error reading {file}: {e}")

# Write to CSV
with open(csv_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Filename", "Rating"])
    writer.writerows(ratings_data)

print(f"\nCSV written to {csv_filename}")

# Extract just the ratings for analysis
ratings = [r[1] for r in ratings_data]

# Compute statistics
if ratings:
    mean_rating = statistics.mean(ratings)
    median_rating = statistics.median(ratings)
    variance_rating = statistics.variance(ratings) if len(ratings) > 1 else 0.0
    std_dev_rating = statistics.stdev(ratings) if len(ratings) > 1 else 0.0

    print("\n--- Rating Statistics ---")
    print(f"Mean:     {mean_rating:.2f}")
    print(f"Median:   {median_rating:.2f}")
    print(f"Variance: {variance_rating:.2f}")
    print(f"Std Dev:  {std_dev_rating:.2f}")
else:
    print("No ratings found.")
