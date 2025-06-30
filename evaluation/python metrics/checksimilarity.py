import os
import csv
from collections import defaultdict
import cv2
from image_similarity_measures.quality_metrics import (
    ssim, psnr, rmse, sam, sre, uiq
)

folderA = "./initial_images"
folderB = "./fewShot_deepseek_output_images"
output_csv = "./image_similarity_results.csv"

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
        stem, _ = os.path.splitext(fname)
        stem_map[stem].append(fname)
    return stem_map

mapA = build_stem_map(folderA)
mapB = build_stem_map(folderB)
all_stems = sorted(set(mapA.keys()).union(set(mapB.keys())))

with open(output_csv, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["ImageName", "SSIM", "PSNR", "RMSE", "SAM", "SRE", "UIQ"])  # Header
    c=0

    for stem in all_stems:
        if stem in mapA and stem in mapB:
            c+=1
            filenameA = mapA[stem][0]
            filenameB = mapB[stem][0]
            pathA = os.path.join(folderA, filenameA)
            pathB = os.path.join(folderB, filenameB)

            imgA = cv2.imread(pathA)
            imgB = cv2.imread(pathB)

            if imgA is None or imgB is None:
                writer.writerow([stem] + ['NA'] * 6)
                continue

            imgB_resized = cv2.resize(imgB, (imgA.shape[1], imgA.shape[0]))
            metrics = compare_images(imgA, imgB_resized)
            writer.writerow([stem] + [f"{float(val):.4f}" for val in metrics.values()])
            print(f"Compared {stem}: {metrics},{c}")
        else:
            # Image unmatched in one folder
            writer.writerow([stem] + ['NA'] * 6)
            print(f"Image {stem} unmatched in one folder, skipping comparison.")