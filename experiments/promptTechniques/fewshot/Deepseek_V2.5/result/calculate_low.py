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
# Mean:     0.7781
# Median:   0.8985
# Variance: 0.0819
# Std Dev:  0.2862

# --- PSNR ---
# Mean:     34.8949
# Median:   36.6000
# Variance: 22.8638
# Std Dev:  4.7816

# --- RMSE ---
# Mean:     0.0214
# Median:   0.0148
# Variance: 0.0002
# Std Dev:  0.0156

# --- SAM ---
# Mean:     0.0000
# Median:   0.0000
# Variance: 0.0000
# Std Dev:  0.0000

# --- SRE ---
# Mean:     56.3823
# Median:   59.1738
# Variance: 81.2208
# Std Dev:  9.0123

# --- UIQ ---
# Mean:     -0.0001
# Median:   0.0001
# Variance: 0.0000
# Std Dev:  0.0010


#UML
# --- SSIM ---
# Mean:     0.7823
# Median:   0.9029
# Variance: 0.0767
# Std Dev:  0.2769

# --- PSNR ---
# Mean:     35.3328
# Median:   37.2826
# Variance: 27.6701
# Std Dev:  5.2602

# --- RMSE ---
# Mean:     0.0210
# Median:   0.0137
# Variance: 0.0003
# Std Dev:  0.0165

# --- SAM ---
# Mean:     0.0000
# Median:   0.0000
# Variance: 0.0000
# Std Dev:  0.0000

# --- SRE ---
# Mean:     56.4554
# Median:   56.9046
# Variance: 45.3621
# Std Dev:  6.7351

# --- UIQ ---
# Mean:     0.0003
# Median:   0.0004
# Variance: 0.0000
# Std Dev:  0.0015