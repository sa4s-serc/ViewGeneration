import pandas as pd

# Read the CSV file
df = pd.read_csv("image_comparisons_cosine_similarity.csv")

# Calculate mean of the column
mean_value = df["vgg16_cosine_similarity"].mean()

# Print result
print("Mean of vgg16_cosine_similarity:", mean_value)
