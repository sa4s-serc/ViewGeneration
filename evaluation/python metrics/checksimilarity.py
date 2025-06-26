import os
from collections import defaultdict
import cv2
from image_similarity_measures.quality_metrics import (
    ssim, psnr, rmse, sam, sre, uiq
)

folderA = "./initial_images"
folderB = "./fewShot_deepseek_output_images"
output_file = "./image_similarity_results.txt"
def compare_images(img1, img2):
    return {
        "SSIM": ssim(img1, img2),
        "PSNR": psnr(img1, img2),
        "RMSE": rmse(img1, img2),
        "SAM": sam(img1, img2),
        "SRE": sre(img1, img2),
        "UIQ": uiq(img1, img2),
    }



# Build maps without extensions
def build_stem_map(folder):
    stem_map = defaultdict(list)
    for fname in os.listdir(folder):
        stem, _ = os.path.splitext(fname)
        stem_map[stem].append(fname)
    return stem_map

mapA = build_stem_map(folderA)
mapB = build_stem_map(folderB)
common_stems = sorted(set(mapA.keys()) & set(mapB.keys()))

with open(output_file, 'w') as f:
    for stem in common_stems:
        filenameA = mapA[stem][0]
        filenameB = mapB[stem][0]
        pathA = os.path.join(folderA, filenameA)
        pathB = os.path.join(folderB, filenameB)

        imgA = cv2.imread(pathA)
        imgB = cv2.imread(pathB)
        imgB_resized = cv2.resize(imgB, (imgA.shape[1], imgA.shape[0]))
        metrics = compare_images(imgA, imgB_resized)

        f.write(f"🔍 {stem}\n")
        for key, val in metrics.items():
            f.write(f"{key}: {float(val):.4f}\n")
        f.write("\n")

    # Log unmatched
    unmatchedA = set(mapA.keys()) - set(mapB.keys())
    for stem in unmatchedA:
        f.write(f"No match for {mapA[stem][0]} in {folderB}\n\n")
