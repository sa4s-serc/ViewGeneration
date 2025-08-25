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
# Mean:     0.8298
# Median:   0.8905
# Variance: 0.0298
# Std Dev:  0.1726

# --- PSNR ---
# Mean:     35.2874
# Median:   36.3191
# Variance: 13.7183
# Std Dev:  3.7038

# --- RMSE ---
# Mean:     0.0190
# Median:   0.0152
# Variance: 0.0001
# Std Dev:  0.0109

# --- SAM ---
# Mean:     7.3924
# Median:   0.0000
# Variance: 655.7724
# Std Dev:  25.6081

# --- SRE ---
# Mean:     56.1431
# Median:   57.1856
# Variance: 42.6913
# Std Dev:  6.5339

# --- UIQ ---
# Mean:     0.0010
# Median:   -0.0002
# Variance: 0.0000
# Std Dev:  0.0023