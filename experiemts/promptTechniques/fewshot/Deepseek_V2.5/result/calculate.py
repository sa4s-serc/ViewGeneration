import csv
import statistics

# Path to your CSV file
csv_file = "image_similarity_results.csv"

# Initialize a dictionary to store each metric's values
metrics_data = {
    "SSIM": [],
    "PSNR": [],
    "RMSE": [],
    "SAM": [],
    "SRE": [],
    "UIQ": []
}

# Read the CSV and collect metric values
with open(csv_file, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        for metric in metrics_data.keys():
            val_str = row.get(metric, "0").strip()
            try:
                val = float(val_str) if val_str.upper() != "NA" else 0.0
            except ValueError:
                val = 0.0
            metrics_data[metric].append(val)

# Compute stats
for metric, values in metrics_data.items():
    mean_val = statistics.mean(values)
    median_val = statistics.median(values)
    variance_val = statistics.variance(values) if len(values) > 1 else 0.0
    std_dev = statistics.stdev(values) if len(values) > 1 else 0.0

    print(f"\n--- {metric} ---")
    print(f"Mean:     {mean_val:.4f}")
    print(f"Median:   {median_val:.4f}")
    print(f"Variance: {variance_val:.4f}")
    print(f"Std Dev:  {std_dev:.4f}")
