import pandas as pd
import numpy as np

# Input CSV file
input_csv = "image_comparisons_cosine_similarity.csv"

# Read CSV
df = pd.read_csv(input_csv)

# Select the similarity column
values = df["vgg16_cosine_similarity"]

# Compute statistics
mean_val = np.mean(values)
median_val = np.median(values)
variance_val = np.var(values, ddof=1)   # sample variance
std_dev_val = np.std(values, ddof=1)    # sample standard deviation

# Print results
print(f"Mean: {mean_val:.6f}")
print(f"Median: {median_val:.6f}")
print(f"Variance: {variance_val:.6f}")
print(f"Standard Deviation: {std_dev_val:.6f}")


# Mean: 0.266525
# Median: 0.283108
# Variance: 0.003420
# Standard Deviation: 0.058477