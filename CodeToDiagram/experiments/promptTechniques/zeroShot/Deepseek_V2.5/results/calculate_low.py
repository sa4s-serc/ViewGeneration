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
# Mean:     0.8349
# Median:   0.9051
# Variance: 0.0439
# Std Dev:  0.2096

# --- PSNR ---
# Mean:     35.4645
# Median:   36.8899
# Variance: 15.2908
# Std Dev:  3.9103

# --- RMSE ---
# Mean:     0.0189
# Median:   0.0143
# Variance: 0.0002
# Std Dev:  0.0122

# --- SAM ---
# Mean:     0.0000
# Median:   0.0000
# Variance: 0.0000
# Std Dev:  0.0000

# --- SRE ---
# Mean:     56.6978
# Median:   60.0694
# Variance: 80.6849
# Std Dev:  8.9825

# --- UIQ ---
# Mean:     -0.0001
# Median:   -0.0001
# Variance: 0.0000
# Std Dev:  0.0012

#UML
# --- SSIM ---
# Mean:     0.8426
# Median:   0.9149
# Variance: 0.0318
# Std Dev:  0.1784

# --- PSNR ---
# Mean:     36.2282
# Median:   37.6403
# Variance: 17.2010
# Std Dev:  4.1474

# --- RMSE ---
# Mean:     0.0176
# Median:   0.0131
# Variance: 0.0001
# Std Dev:  0.0121

# --- SAM ---
# Mean:     0.0000
# Median:   0.0000
# Variance: 0.0000
# Std Dev:  0.0000

# --- SRE ---
# Mean:     56.9006
# Median:   57.8574
# Variance: 44.3425
# Std Dev:  6.6590

# --- UIQ ---
# Mean:     -0.0008
# Median:   -0.0006
# Variance: 0.0000
# Std Dev:  0.0013