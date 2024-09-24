import os
import requests
import mimetypes
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Create a session for making requests with headers
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
})

def fetch_html(url):
    try:
        response = session.get(url)
        response.raise_for_status() # Check for HTTP errors
        return response.text
    except requests.exceptions.HTTPError as http_err:
        print (f"HTTP error occurred: {http_err} - Status Code: {response.status_code}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    return None
    
def parse_images(html, base_url):

    soup = BeautifulSoup(html, 'lxml')
    img_tags = soup.find_all('img')

    # Build absolute URLs for images
    img_urls = set() # Use a set to avoid duplicates
    for img in img_tags:
        img_url = img.get('src') or img.get('data-src') or img.get('data-lazy')  # Handle lazy-loaded images
        if img_url:
            # Convert relative URLs to absolute URLs
            img_url = urljoin(base_url, img_url)

            # Only include URLs that seem to be actual image files
            if img_url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')):
                img_urls.add(img_url)  # Set ensures no duplicate URLs
    return img_urls

def download_images (img_urls, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for i, img_url in enumerate(img_urls):
        try:

            # Check if the URL is accessible before downloading
            response = session.head(img_url)
            response.raise_for_status()

            # Determine the content type and set the file extension
            content_type = response.headers.get('content-type')
            extension = mimetypes.guess_extension(content_type) or '.jpg'

            # Download the image data
            img_data = session.get(img_url).content
            img_name = os.path.join(destination_folder, f'image_{i+1}{extension}')

            # Save the image to the destination folder
            with open (img_name, 'wb') as f:
                f.write(img_data)
            print (f"Downloaded {img_name}")

        except requests.exceptions.RequestException as e:
            print (f"Error downloading {img_url}: {e}")