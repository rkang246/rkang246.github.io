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
    "oBIZrig",
    "iJ3neR5"] # Update with all galleries to be pulled from

PHOTOS_PER_PAGE = 15
OUTPUT_DIR = "_includes/photos"

class ImgurImage:
    def __init__(self, url, description):
        self.url = url
        self.description = description

    def __repr__(self):
        return f"ImgurImage(url={self.url}, description={self.description})"

# Returns list of ImgurImage from imgur API
def call_gallery_api(client_id, gallery_id):
    url = f"https://api.imgur.com/3/album/{gallery_id}/images"
    headers = {"Authorization": f"Client-ID {client_id}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    
    if not data.get("success", False):
        print("Error fetching gallery:", data.get("data", {}).get("error", "Unknown error"))
        return []
    
    photos = data.get("data", [])
    print(data)
    imgur_images = [(photo["link"], photo["description"]) for photo in photos if "link" in photo]
    
    return imgur_images

def fetch_imgur_images():
    imgur_images = []
    for gallery_id in GALLERY_IDS:
        batch = call_gallery_api(IMGUR_CLIENT_ID, gallery_id)
        if len(batch) == 0:
            exit(1)
        imgur_images.extend(batch)
    return imgur_images

# Return (title, location)
# Description is expected to be "title,sublocation,location", "sublocation,location", or empty
def parse_description(description):
    if description is None:
        return None

    description = description.split(",")
    if len(description) == 2:
        return ("", f"{description[0].strip()}, {description[1].strip()}")
    elif len(description) == 3:
        return (description[0].strip(), f"{description[1].strip()}, {description[2].strip()}")
    
    return None

# build _includes/photos
def write_photogrid_batch(batch_images, batch_num):
    if batch_num == 1:
        filename = "photogrid.html"
    else:
        filename = f"photogrid{batch_num}.html"

    filepath = os.path.join(OUTPUT_DIR, filename)

    photogrid_html = []
    for image in batch_images:
        url = image[0]
        
        photogrid_html.append('  <div class="grid__item">')

        # Build media element (image vs video)
        if url.endswith('.mp4'):
            media_element = [
                '      <video autoplay loop muted playsinline>',
                f'        <source src="{url}" type="video/mp4">',
                '        Your browser does not support the video tag.',
                '      </video>'
            ]
        else:
            media_element = [f'      <img src="{url}" loading="lazy" alt="">']
        
        # Build photo caption (if exists)
        description = parse_description(image[1])
        # If no description, output media element directly
        if description is None:
            media_element = [s[2:] if s.startswith('  ') else s for s in media_element] # trim 2 spaces for formatting
            photogrid_html.extend(media_element)
        else:
            title, location = description

            photogrid_html.append('    <label class="click-toggle">')
            photogrid_html.append('      <input type="checkbox" hidden>')
            photogrid_html.extend(media_element)

            photogrid_html.append('      <span class="caption">')
            if title:
                photogrid_html.append(f'        <span class="title">{title}</span>')
            photogrid_html.append('        <span class="location">')
            photogrid_html.append('          <i class="fa-solid fa-location-dot"></i>')
            photogrid_html.append(f'          {location}')
            photogrid_html.append('        </span>')
            photogrid_html.append('      </span>')

            photogrid_html.append('    </label>')

        photogrid_html.append('  </div>')

    # Overwrite content into jekyll template
    with open(filepath, "w", encoding="utf-8") as file:
        file.write("\n".join(photogrid_html))

    print(f"Generated {filename} with {len(batch_images)} items.")

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
    images = fetch_imgur_images()
    print(f"Successfully loaded {len(images)} from imgur api")

    total = len(images)
    num_pages = math.ceil(total / PHOTOS_PER_PAGE) # Calculate number of pages to divide

    # Create photogrid html in batch pages for pagination
    for page in range(num_pages):
        start = page * PHOTOS_PER_PAGE
        end = start + PHOTOS_PER_PAGE
        batch_images = images[start:end]
        write_photogrid_batch(batch_images, page + 1)
        write_photogrid_wrapper(page + 1)
    print(f"Successfully built {num_pages} photogrid files from {total} images/videos.")

if __name__ == "__main__":
    main()
