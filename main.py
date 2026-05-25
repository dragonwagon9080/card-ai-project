import requests
from pathlib import Path
from bs4 import BeautifulSoup
import re

# -----------------------
# eBay listing URL
# -----------------------
url = "https://www.ebay.com/itm/366423491987"

# -----------------------
# Folder setup
# -----------------------
output_folder = Path("images")
output_folder.mkdir(exist_ok=True)

# -----------------------
# Browser headers (bypass 403)
# -----------------------
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}

session = requests.Session()

# -----------------------
# Get eBay page
# -----------------------
response = session.get(url, headers=headers)

if response.status_code != 200:
    print("Failed to load page:", response.status_code)
    exit()

html = response.text

# -----------------------
# Extract images (more reliable method)
# -----------------------
soup = BeautifulSoup(html, "html.parser")

image_urls = []

for img in soup.find_all("img"):
    src = img.get("src")

    if not src:
        continue

    if "i.ebayimg.com" in src and src.endswith(".jpg"):
        # upgrade resolution if possible
        src = re.sub(r"s-l\d+", "s-l1600", src)

        if src not in image_urls:
            image_urls.append(src)

print(f"Found {len(image_urls)} images")

if len(image_urls) == 0:
    print("No images found. eBay likely blocked extraction.")
    exit()

# -----------------------
# Download images (front/back aware)
# -----------------------
for i, img_url in enumerate(image_urls[:5]):
    try:
        img_data = session.get(img_url, headers=headers).content

        if i == 0:
            filename = "front.jpg"
        elif i == 1:
            filename = "back.jpg"
        else:
            filename = f"extra_{i}.jpg"

        file_path = output_folder / filename

        with open(file_path, "wb") as f:
            f.write(img_data)

        print("Saved:", filename)

    except Exception as e:
        print("Error downloading image:", e)

print("\nDone. Images ready for AI pipeline.")