import requests
import os
import math

"""
Idempotent build script for static image gallery :D

Builds multiple pages for infinite scroll + masonry layout
- _includes/photos: contains raw images
- photo-html: contains jekyll wrapper for each page
"""

IMGUR_CLIENT_ID = "f918a83cac0b5da"
GALLERY_IDS = [
    # "nSu6lcA"
    "oBIZrig"] # Update with all galleries to be pulled from

PHOTOS_PER_PAGE = 10
OUTPUT_DIR = "_includes/photos"

def call_gallery_api(client_id, gallery_id):
    url = f"https://api.imgur.com/3/album/{gallery_id}/images"
    headers = {"Authorization": f"Client-ID {client_id}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    
    if not data.get("success", False):
        print("Error fetching gallery:", data.get("data", {}).get("error", "Unknown error"))
        return []
    
    photos = data.get("data", [])
    urls = [photo["link"] for photo in photos if "link" in photo]
    
    return urls

def fetch_image_urls():
    urls = []
    for gallery_id in GALLERY_IDS:
        batch = call_gallery_api(IMGUR_CLIENT_ID, gallery_id)
        if len(batch) == 0:
            exit(1)
        urls.extend(batch)
    return urls

# build _includes/photos
def write_photogrid_batch(batch_urls, batch_num):
    if batch_num == 1:
        filename = "photogrid.html"
    else:
        filename = f"photogrid{batch_num}.html"

    filepath = os.path.join(OUTPUT_DIR, filename)

    photogrid_html = []
    for url in batch_urls:
        photogrid_html.append('  <div class="grid__item">')
        if url.endswith('.mp4'):
            photogrid_html.append('    <video autoplay loop muted playsinline>')
            photogrid_html.append(f'      <source src="{url}" type="video/mp4">')
            photogrid_html.append('      Your browser does not support the video tag.')
            photogrid_html.append('    </video>')
        else:
            photogrid_html.append(f'    <img src="{url}" loading="lazy" alt="">')
        photogrid_html.append('  </div>')


    # Overwrite content into jekyll template
    with open(filepath, "w", encoding="utf-8") as file:
        file.write("\n".join(photogrid_html))

    print(f"Generated {filename} with {len(batch_urls)} items.")

# build photo-html wrappers
def write_photogrid_wrapper(batch_num):
    if batch_num == 1:
        # First batch is already included manually in photo-gallery.html
        return
    wrapper_filename = f"photogrid{batch_num}.md"
    wrapper_path = os.path.join("photo-html", wrapper_filename)

    # Create the "photos" directory if it doesn't exist
    if not os.path.exists("photo-html"):
        os.makedirs("photo-html")

    with open(wrapper_path, "w", encoding="utf-8") as f:
        f.write(f"""---
layout: none
permalink: /photo-html/photogrid{batch_num}.html
---
{{% include photos/photogrid{batch_num}.html %}}
""")
    print(f"Generated wrapper: {wrapper_path}")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Fetch all URLs
    urls = fetch_image_urls()
    print(f"Successfully loaded {len(urls)} from imgur api")

    total = len(urls)
    num_pages = math.ceil(total / PHOTOS_PER_PAGE) # Calculate number of pages to divide

    # Create photogrid html in batch pages for pagination
    for page in range(num_pages):
        start = page * PHOTOS_PER_PAGE
        end = start + PHOTOS_PER_PAGE
        batch_urls = urls[start:end]
        write_photogrid_batch(batch_urls, page + 1)
        write_photogrid_wrapper(page + 1)
    print(f"Successfully built {num_pages} photogrid files from {total} images/videos.")

if __name__ == "__main__":
    main()
