import csv
import json
import statistics

# Paths
low_granularity_file = "../../../../Architectural_knowledge_extraction/UML.jsonl"
csv_file = "oneShot_claude_output_images_similarity_results.csv"

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
# Mean:     0.8366
# Median:   0.9113
# Variance: 0.0520
# Std Dev:  0.2281

# --- PSNR ---
# Mean:     35.7866
# Median:   36.6950
# Variance: 14.4033
# Std Dev:  3.7952

# --- RMSE ---
# Mean:     0.0183
# Median:   0.0146
# Variance: 0.0002
# Std Dev:  0.0127

# --- SAM ---
# Mean:     4.0881
# Median:   0.0000
# Variance: 367.6714
# Std Dev:  19.1748

# --- SRE ---
# Mean:     57.4407
# Median:   60.4489
# Variance: 74.1043
# Std Dev:  8.6084

# --- UIQ ---
# Mean:     0.0001
# Median:   -0.0001
# Variance: 0.0000
# Std Dev:  0.0015


#UML
# --- SSIM ---
# Mean:     0.8858
# Median:   0.9135
# Variance: 0.0074
# Std Dev:  0.0858

# --- PSNR ---
# Mean:     37.0211
# Median:   37.6458
# Variance: 7.2910
# Std Dev:  2.7002

# --- RMSE ---
# Mean:     0.0149
# Median:   0.0131
# Variance: 0.0000
# Std Dev:  0.0066

# --- SAM ---
# Mean:     0.0000
# Median:   0.0000
# Variance: 0.0000
# Std Dev:  0.0000

# --- SRE ---
# Mean:     58.4551
# Median:   58.2783
# Variance: 12.0783
# Std Dev:  3.4754

# --- UIQ ---
# Mean:     0.0001
# Median:   -0.0001
# Variance: 0.0000
# Std Dev:  0.0022