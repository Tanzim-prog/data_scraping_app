import os
import time
import requests
import mimetypes
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from webdriver_setup import get_webdriver 

# Create a session for making requests with headers
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
})

# Fetch and render the full page using Selenium
def fetch_html(url, driver):
    driver.get(url)
    time.sleep(5) # Wait for the page to load

    # Scroll to load lazy-loaded images
    scroll_pause_time = 3
    last_height = driver.execute_script("return document.body.scrollHeight")

    for _ in range(5): # Scroll multiple times
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Return the full HTML after scrolling
    return driver.page_source

# Parse the images using BeautifulSoup
def parse_images(html, base_url):

    soup = BeautifulSoup(html, 'lxml')
    img_tags = soup.find_all('img')

    print(f"Found {len(img_tags)} image tags.")  # Log the number of image tags found

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

    print(f"Total unique image URLs found: {len(img_urls)}")  # Log the number of unique image URLs found           
    return img_urls

# Download the images
def download_images (img_urls, destination_folder, count_callback=None):
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
            
            # Callback to update image count
            if count_callback:
                count_callback(i + 1)

        except requests.exceptions.RequestException as e:
            print (f"Error downloading {img_url}: {e}")

# Main Function
def scrape_images(url, destination_folder, count_callback=None):
    driver = get_webdriver(headless=True) # Set up the Selenium driver
    try:
        html = fetch_html(url, driver)
        img_urls = parse_images(html, url)
        if img_urls:
            download_images(img_urls, destination_folder, count_callback)
            print(f"Successfully downloaded {len(img_urls)} images to {destination_folder}")
        else:
            print("No images found.")
    finally:
        driver.quit()  # Make sure to close the driver