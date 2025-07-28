import csv
import re

input_file = "results.txt"  # Replace with your actual file path
output_file = "similarity_results.csv"

# Regex pattern without capturing the index
pattern = re.compile(
    r"^(?P<repo>[\w\-]+): \{"
    r"'SSIM': (?P<SSIM>[\d\.e\-]+), 'PSNR': (?P<PSNR>[\d\.e\-]+), 'RMSE': (?P<RMSE>[\d\.e\-]+), "
    r"'SAM': (?P<SAM>[\d\.e\-]+), 'SRE': (?P<SRE>[\d\.e\-]+), 'UIQ': (?P<UIQ>[\-\d\.e]+)"
)

data = []

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        match = pattern.search(line.strip())
        if match:
            result = match.groupdict()
            data.append(result)

# Write to CSV
with open(output_file, "w", newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["repo", "SSIM", "PSNR", "RMSE", "SAM", "SRE", "UIQ"])
    writer.writeheader()
    writer.writerows(data)

print(f"✅ CSV file created: {output_file}")

