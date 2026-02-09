import csv
import statistics

# Path to your CSV file
csv_file = "fewShot_deepseek_output_images_similarity_results.csv"

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
