import csv
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from tqdm import tqdm

CSV_FILE = '/Users/user/Desktop/coding/WIP/samevibe/published_images.csv'
OUTPUT_DIR = '/Users/user/Desktop/coding/WIP/samevibe/data'
MAX_IMAGES = 1000

def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return True
    return False

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(CSV_FILE, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        urls = [row['iiifthumburl'] for row in reader][:MAX_IMAGES]

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for i, url in enumerate(urls):
            filename = os.path.join(OUTPUT_DIR, f'image_{i:04d}.jpg')
            futures.append(executor.submit(download_image, url, filename))

        with tqdm(total=len(futures), desc="Downloading images") as pbar:
            for future in as_completed(futures):
                pbar.update(1)

    print(f"Downloaded {len(urls)} images to {OUTPUT_DIR}")

if __name__ == '__main__':
    main()
