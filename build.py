import requests

"""
Idempotent build script for static image gallery :D
"""

IMGUR_CLIENT_ID = "f918a83cac0b5da"
GALLERY_IDS = [
    # "nSu6lcA"
    "oBIZrig"] # Update with all galleries to be pulled from


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

def main():
    # Fetch all URLs
    urls = fetch_image_urls()

    # Load HTML
    with open("photo-gallery.html", "r", encoding="utf-8") as file:
        content = file.readlines()
    
    # Remove existing photogrid content
    inside_photogrid = False
    new_content = []
    start_index = None

    for i, line in enumerate(content):
        if "<!-- Photogrid -->" in line:
            if start_index is None:
                start_index = i  # Store the index of the first occurrence
            inside_photogrid = not inside_photogrid  # Toggle state
            new_content.append(line.rstrip())  # Keep the comment lines
        elif not inside_photogrid:
            new_content.append(line.rstrip())  # Preserve formatting

    # Generate new photogrid content
    photogrid_html = '      <div class="masonry-container">\n'
    for url in urls:
        photogrid_html += f'        <div class="masonry-item">\n'
        if 'mp4' in url:
            photogrid_html += f'          <video autoplay loop muted playsinline>\n'
            photogrid_html += f'            <source src="{url}" type="video/mp4">\n'
            photogrid_html += f'            Your browser does not support the video tag.\n'
            photogrid_html += f'          </video>\n'

        else:
            photogrid_html += f'          <img src="{url}" loading="lazy" />\n'
        photogrid_html += f'        </div>\n'
    photogrid_html += '      </div>\n'

    # Ensure the start index exists before inserting
    if start_index is not None:
        new_content.insert(start_index + 1, photogrid_html.strip())

    # Write the modified content back to the file
    # print(new_content)
    with open("photo-gallery.html", "w", encoding="utf-8") as file:
        file.write("\n".join(new_content) + "\n")

    print(f"Successfully loaded {len(urls)} from imgur api")


if __name__ == "__main__":
    main()
