import os
from image_similarity_measures.quality_metrics import (
    ssim, psnr, rmse, sam, sre, uqi, vifp
)
import cv2

# Paths to your folders
folderA = "/home/sathvika/CodeToDiagram/chatgpt_tree_result/initial_images"
folderB = "/home/sathvika/CodeToDiagram/chatgpt_tree_result/output_images"

# Function to calculate all metrics
def compare_images(img1, img2):
    return {
        "SSIM": ssim(img1, img2),
        "PSNR": psnr(img1, img2),
        "RMSE": rmse(img1, img2),
        "SAM": sam(img1, img2),
        "SRE": sre(img1, img2),
        "UQI": uqi(img1, img2),
        "VIFP": vifp(img1, img2)
    }

# Loop through matching files
files = sorted(os.listdir(folderA))
for filename in files:
    pathA = os.path.join(folderA, filename)
    pathB = os.path.join(folderB, filename)
    if os.path.exists(pathB):
        imgA = cv2.imread(pathA)
        imgB = cv2.imread(pathB)
        metrics = compare_images(imgA, imgB)
        print(f"🔍 {filename}")
        for key, val in metrics.items():
            print(f"   {key}: {float(val):.4f}")
    else:
        print(f"⚠️  No match for {filename} in output_images")
