
'''This script downloads images from a CSV file containing image URLs and repository names.
It handles GitHub blob URLs, ensures the correct file extension is used, and saves images in a specified directory.These are the ground truth initial images
'''

import csv
import os
import requests
from urllib.parse import urlparse
import mimetypes

def convert_github_blob_to_raw(url):
    if "github.com" in url and "/blob/" in url:
        return url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    return url

def get_file_extension_from_url_or_response(url, response):
    parsed = urlparse(url)
    ext = os.path.splitext(parsed.path)[1]
    if ext:
        return ext
    content_type = response.headers.get('Content-Type')
    return mimetypes.guess_extension(content_type) or ".png"

def sanitize_repo_name(repo_name):
    return repo_name.replace('/', '_').replace('\\', '_').rstrip('_')

def download_image(url, repo_name, save_dir="initial_images"):
    os.makedirs(save_dir, exist_ok=True)
    raw_url = convert_github_blob_to_raw(url)
    try:
        response = requests.get(raw_url, stream=True)
        response.raise_for_status()
        ext = get_file_extension_from_url_or_response(raw_url, response)
        safe_repo_name = sanitize_repo_name(repo_name)
        filename = f"{safe_repo_name}{ext}"
        filepath = os.path.join(save_dir, filename)
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def download_images_from_csv(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for i, row in enumerate(reader):
            image_url = row.get("Image URL")
            repo_name = row.get("Repository Name")
            if image_url and repo_name:
                download_image(image_url, repo_name)

# Usage
if __name__ == "__main__":
    csv_file = "filtered_dataset.csv"  
    download_images_from_csv(csv_file)
