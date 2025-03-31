import requests

# Replace with your actual Imgur Client ID
IMGUR_CLIENT_ID = "f918a83cac0b5da"
GALLERY_IDS = ["nSu6lcA"] # Update with all galleries to be pulled from


def fetch_gallery_photos(client_id, gallery_id):
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


def main():
    # Fetch all URLs
    urls = []
    for gallery_id in GALLERY_IDS:
        batch = fetch_gallery_photos(IMGUR_CLIENT_ID, gallery_id)
        if len(batch) == 0:
            exit(1)
        urls.extend(batch)
    
    


if __name__ == "__main__":
    main()
