
'''This script compares images in two folders and calculates various similarity metrics.
It generates a CSV file with the results, including SSIM, PSNR, RMSE, SAM, SRE, and UIQ.
The script handles images with the same stem name in both folders, resizing them as necessary.
It skips images that are already present in the output CSV file to avoid redundant comparisons.
'''
import os
import csv
from collections import defaultdict
import cv2
from image_similarity_measures.quality_metrics import (
    ssim, psnr, rmse, sam, sre, uiq
)

folderA = "./initial_images"
folderB = "./output_images"
output_csv = f"./{os.path.basename(folderB.rstrip('/'))}_similarity_results.csv"


# List of valid image extensions
valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')

def compare_images(img1, img2):
    return {
        "SSIM": ssim(img1, img2),
        "PSNR": psnr(img1, img2),
        "RMSE": rmse(img1, img2),
        "SAM": sam(img1, img2),
        "SRE": sre(img1, img2),
        "UIQ": uiq(img1, img2),
    }

def build_stem_map(folder):
    stem_map = defaultdict(list)
    for fname in os.listdir(folder):
        if not fname.lower().endswith(valid_extensions):
            continue  # Skip non-image files
        stem = os.path.splitext(fname)[0]
        stem_map[stem].append(fname)
    return stem_map

# Build image maps
mapA = build_stem_map(folderA)
mapB = build_stem_map(folderB)
all_stems = sorted(set(mapA.keys()).union(set(mapB.keys())))

# Load existing CSV data if any
existing_stems = set()
if os.path.exists(output_csv):
    with open(output_csv, 'r') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)  # Skip header
        except StopIteration:
            header = None  # Empty file
        for row in reader:
            if row and row[0]:
                existing_stems.add(row[0])

# Open CSV for appending results
with open(output_csv, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    if not existing_stems:
        writer.writerow(["ImageName", "SSIM", "PSNR", "RMSE", "SAM", "SRE", "UIQ"])

    compared_count = 0
    for stem in all_stems:
        if stem in existing_stems:
            print(f"Skipping {stem}, already in CSV.")
            continue

        if stem in mapA and stem in mapB:
            filenameA = mapA[stem][0]
            filenameB = mapB[stem][0]
            pathA = os.path.join(folderA, filenameA)
            pathB = os.path.join(folderB, filenameB)

            imgA = cv2.imread(pathA)
            imgB = cv2.imread(pathB)

            if imgA is None or imgB is None:
                print(f"⚠️ Warning: Could not load image(s) for '{stem}'")
                writer.writerow([stem] + ['NA'] * 6)
                csvfile.flush()
                continue

            # Resize and compare
            imgB_resized = cv2.resize(imgB, (imgA.shape[1], imgA.shape[0]))
            metrics = compare_images(imgA, imgB_resized)
            writer.writerow([stem] + [f"{float(val):.4f}" for val in metrics.values()])
            csvfile.flush()
            compared_count += 1
            print(f"✅ Compared {stem}: {metrics} (#{compared_count})")
        else:
            print(f"❌ Image '{stem}' unmatched in one folder, skipping.")
            writer.writerow([stem] + ['NA'] * 6)
            csvfile.flush()


print(f"\n✅ Comparison complete. Total image pairs compared: {compared_count}")
