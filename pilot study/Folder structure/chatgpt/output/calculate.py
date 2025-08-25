import csv
import statistics

# Path to your CSV file
csv_file = "output_images_similarity_results.csv"

# List of metric columns
metric_keys = ["SSIM", "PSNR", "RMSE", "SAM", "SRE", "UIQ"]

# Dictionary to hold filtered metric data
metrics_data = {key: [] for key in metric_keys}

# Read CSV and filter out rows with all NaNs in metric columns
with open(csv_file, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Check if all metrics are NA or empty
        if all(not row[key].strip() or row[key].strip().upper() == "NA" for key in metric_keys):
            continue  # skip this row

        # Otherwise, process the valid values
        for key in metric_keys:
            val_str = row.get(key, "").strip()
            try:
                val = float(val_str) if val_str.upper() != "NA" and val_str != "" else 0.0
            except ValueError:
                val = 0.0
            metrics_data[key].append(val)

# Compute and display statistics
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
# Mean:     0.8006
# Median:   0.8891
# Variance: 0.0478
# Std Dev:  0.2187

# --- PSNR ---
# Mean:     35.1026
# Median:   36.5638
# Variance: 20.6290
# Std Dev:  4.5419

# --- RMSE ---
# Mean:     0.0204
# Median:   0.0149
# Variance: 0.0002
# Std Dev:  0.0138

# --- SAM ---
# Mean:     0.0000
# Median:   0.0000
# Variance: 0.0000
# Std Dev:  0.0000

# --- SRE ---
# Mean:     55.8483
# Median:   57.1113
# Variance: 49.8010
# Std Dev:  7.0570

# --- UIQ ---
# Mean:     -0.0008
# Median:   -0.0001
# Variance: 0.0000
# Std Dev:  0.0025