import os
import cv2
from image_similarity_measures.quality_metrics import (
    ssim, psnr, rmse, sam, sre, uiq
)

folderA = "/home/sathvika/CodeToDiagram/Approach 4/gemini-2o/output/gemini_output_images"
folderB = "/home/sathvika/CodeToDiagram/scripts/initial_images"
output_file = "/home/sathvika/CodeToDiagram/Approach 4/gemini-2o/output/image_similarity_results.txt"
def compare_images(img1, img2):
    return {
        "SSIM": ssim(img1, img2),
        "PSNR": psnr(img1, img2),
        "RMSE": rmse(img1, img2),
        "SAM": sam(img1, img2),
        "SRE": sre(img1, img2),
        "UIQ": uiq(img1, img2),
    }

files = sorted(os.listdir(folderA))
with open(output_file, 'w') as f:
    for filename in files:
        pathA = os.path.join(folderA, filename)
        pathB = os.path.join(folderB, filename)
        if os.path.exists(pathB):
            imgA = cv2.imread(pathA)
            imgB = cv2.imread(pathB)
            imgB_resized = cv2.resize(imgB, (imgA.shape[1], imgA.shape[0]))
            metrics = compare_images(imgA, imgB_resized)
            
            f.write(f"🔍 {filename}\n")
            for key, val in metrics.items():
                f.write(f"{key}: {float(val):.4f}\n")
            f.write("\n")
        else:
            f.write(f"No match for {filename} in output_images\n\n")
