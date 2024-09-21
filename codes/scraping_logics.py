import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from flask import Flask, render_template

def fetch_html(url):
    ""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        }
        response = requests.get(url, headers = headers)
        response.raise_for_status() # Check for HTTP errors
        return response.text
    except requests.exceptions.RequestException as e:
        print (f"Error fetching {url}: {e}")
        return None
    
def parse_images(html, base_url):

    soup = BeautifulSoup(html, 'lxml')
    img_tags = soup.find_all('img')
    img_urls = []

    for img in img_tags:
        img_url = img.get('src')
        if img_url:
            img_url = urljoin(base_url, img_url) # Convert relative URLs to absolute URLs
            img_urls.append(img_url)
    return img_url

def download_images(img_urls, destination_folder):
    
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for i, img_url in enumerate(img_urls):
        try:
            img_data = requests.get(img_url).content
            img_name = os.path.join(destination_folder, f'image_{i+1}.jpg')
            with open (img_name, 'wb') as f:
                f.write(img_data)
            print (f"Downloaded {img_name}")
        except requests.exceptions.RequestException as e:
            print (f"Error downloading {img_url}: {e}")