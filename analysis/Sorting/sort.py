import pandas as pd

# Input/output file
input_file = "image_comparisons_cosine_similarity.csv"
output_file = "metrics_sorted.csv"

# Load CSV
df = pd.read_csv(input_file)

# 🔹 Sort by a chosen column (e.g., SSIM descending, higher is better)
df_sorted = df.sort_values(by="vgg16_cosine_similarity", ascending=False)

# Save sorted CSV
df_sorted.to_csv(output_file, index=False)

print(f"✅ Sorted file saved as {output_file}")
