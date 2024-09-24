import os
from flask import Flask, request, render_template, redirect, url_for
from scraping_logics import fetch_html, parse_images, download_images

# Specify custom template directory
template_directory = os.path.abspath ("D:/Projects/Data Scraping Application/templates")

app = Flask(__name__, template_folder = template_directory)

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        url = request.form.get('url')
        destination_folder = request.form.get('destination')

        # Validate user inputs
        if not url or not destination_folder:
            return 'Both URL and destination folder are required.', 400
        
        # Fetch HTML content from the provided URL
        html = fetch_html(url)
        if html:
            # Parse images from the HTML
            img_urls = parse_images(html, url)
            if img_urls:
                try:
                    download_images (img_urls, destination_folder)
                    return f'Successfully downloaded {len(img_urls)} images to {destination_folder}'
                except Exception as e:
                    return f'Error downloading images: {e}', 500
            else:
                return 'No images found at the provided URL.', 404
        else:
            return 'Failed to retrieve the webpage. Please check the URL and try again.', 400
        
    return render_template ('index.html')

if __name__ == '__main__':
    app.run(debug = True)