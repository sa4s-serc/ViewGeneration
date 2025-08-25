import csv
import json
import statistics

# Paths
low_granularity_file = "../../../../Architectural_knowledge_extraction/UML.jsonl"
csv_file = "zeroShot_gpt_output_images_similarity_results.csv"

# Step 1: Load low granularity repo names
low_granularity_repos = set()
with open(low_granularity_file, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            data = json.loads(line)
            repo_name = data.get("Repository Name", "").strip()
            if repo_name:
                repo_name_clean = repo_name.replace("/", "_").replace("\\", "_").rstrip("_")
                low_granularity_repos.add(repo_name_clean)

# Step 2: Metric keys
metric_keys = ["SSIM", "PSNR", "RMSE", "SAM", "SRE", "UIQ"]
metrics_data = {key: [] for key in metric_keys}

# Step 3: Read CSV and filter only low-granularity repos
with open(csv_file, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        repo_in_csv = row.get("ImageName", "").strip()
        if repo_in_csv in low_granularity_repos:
            if all(not row[key].strip() or row[key].strip().upper() == "NA" for key in metric_keys):
                continue  # skip empty metrics

            for key in metric_keys:
                val_str = row.get(key, "").strip()
                try:
                    val = float(val_str) if val_str.upper() != "NA" and val_str != "" else 0.0
                except ValueError:
                    val = 0.0
                metrics_data[key].append(val)

# Step 4: Print statistics
for key, values in metrics_data.items():
    if not values:
        print(f"\n--- {key} ---\nNo valid values.")
        continue

    mean_val = statistics.mean(values)
    median_val = statistics.median(values)
    variance_val = statistics.variance(values) if len(values) > 1 else 0.0
    std_dev = statistics.stdev(values) if len(values) > 1 else 0.0

    print(f"\n--- {key} ---")
    print(f"Mean:     {mean_val:.4f}")
    print(f"Median:   {median_val:.4f}")
    print(f"Variance: {variance_val:.4f}")
    print(f"Std Dev:  {std_dev:.4f}")



# --- SSIM ---
# Mean:     0.8145
# Median:   0.9075
# Variance: 0.0591
# Std Dev:  0.2430

# --- PSNR ---
# Mean:     35.3032
# Median:   36.9113
# Variance: 18.7907
# Std Dev:  4.3348

# --- RMSE ---
# Mean:     0.0199
# Median:   0.0143
# Variance: 0.0002
# Std Dev:  0.0141

# --- SAM ---
# Mean:     0.0000
# Median:   0.0000
# Variance: 0.0000
# Std Dev:  0.0000

# --- SRE ---
# Mean:     56.5908
# Median:   59.9088
# Variance: 84.6449
# Std Dev:  9.2003

# --- UIQ ---
# Mean:     0.0003
# Median:   -0.0001
# Variance: 0.0000
# Std Dev:  0.0019


# UML

# --- SSIM ---
# Mean:     0.8410
# Median:   0.8936
# Variance: 0.0314
# Std Dev:  0.1772

# --- PSNR ---
# Mean:     36.1763
# Median:   36.9744
# Variance: 16.5929
# Std Dev:  4.0734

# --- RMSE ---
# Mean:     0.0176
# Median:   0.0142
# Variance: 0.0001
# Std Dev:  0.0118

# --- SAM ---
# Mean:     0.0000
# Median:   0.0000
# Variance: 0.0000
# Std Dev:  0.0000

# --- SRE ---
# Mean:     56.8745
# Median:   58.1637
# Variance: 43.8002
# Std Dev:  6.6182

# --- UIQ ---
# Mean:     0.0007
# Median:   0.0002
# Variance: 0.0000
# Std Dev:  0.0019