'''
This script reads the CSV file containing the VGG16 cosine similarity scores and calculates the mean similarity across all 
image pairs. The mean similarity provides an overall measure of how closely the generated views match the ground truth views in 
terms of visual features as captured by the VGG16 model.
'''
import csv

def calculate_mean_similarity(csv_path):
    similarities = []

    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                similarity = float(row['vgg16_cosine_similarity'])
                similarities.append(similarity)
            except ValueError:
                continue  # Skip if the value is not a valid float

    if not similarities:
        return None  # Avoid division by zero

    mean_similarity = sum(similarities) / len(similarities)
    return mean_similarity

# Example usage:
csv_file = 'image_comparisons_cosine_similarity.csv'  
mean = calculate_mean_similarity(csv_file)
print(f"Mean VGG16 Cosine Similarity: {mean:.6f}")
