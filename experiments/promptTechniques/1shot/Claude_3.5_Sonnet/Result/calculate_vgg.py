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
csv_file = 'image_comparisons_cosine_similarity.csv'  # Replace with the actual file path
mean = calculate_mean_similarity(csv_file)
print(f"Mean VGG16 Cosine Similarity: {mean:.6f}")
