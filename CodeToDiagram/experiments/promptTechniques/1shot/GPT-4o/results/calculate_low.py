import csv
import json
import statistics

# Paths
low_granularity_file = "../../../../Architectural_knowledge_extraction/UML.jsonl"
csv_file = "image_similarity_results.csv"

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
# Mean:     0.8100
# Median:   0.9002
# Variance: 0.0580
# Std Dev:  0.2408

# --- PSNR ---
# Mean:     34.8636
# Median:   36.1345
# Variance: 16.2148
# Std Dev:  4.0268

# --- RMSE ---
# Mean:     0.0205
# Median:   0.0155
# Variance: 0.0002
# Std Dev:  0.0136

# --- SAM ---
# Mean:     0.0000
# Median:   0.0000
# Variance: 0.0000
# Std Dev:  0.0000

# --- SRE ---
# Mean:     56.3548
# Median:   59.2438
# Variance: 82.0417
# Std Dev:  9.0577

# --- UIQ ---
# Mean:     0.0000
# Median:   0.0001
# Variance: 0.0000
# Std Dev:  0.0011


# UML
# --- SSIM ---
# Mean:     0.8333
# Median:   0.9029
# Variance: 0.0336
# Std Dev:  0.1832

# --- PSNR ---
# Mean:     35.3562
# Median:   36.6390
# Variance: 15.4374
# Std Dev:  3.9290

# --- RMSE ---
# Mean:     0.0191
# Median:   0.0147
# Variance: 0.0001
# Std Dev:  0.0118

# --- SAM ---
# Mean:     0.0000
# Median:   0.0000
# Variance: 0.0000
# Std Dev:  0.0000

# --- SRE ---
# Mean:     56.5498
# Median:   58.2913
# Variance: 44.8594
# Std Dev:  6.6977

# --- UIQ ---
# Mean:     0.0001
# Median:   0.0003
# Variance: 0.0000
# Std Dev:  0.0013