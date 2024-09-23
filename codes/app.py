import os
from flask import Flask, request, render_template, redirect, url_for
from scraping_logics import fetch_html, parse_images, download_images

template_directory = os.path.abspath ("D:/Projects/Data Scraping Application/templates")

app = Flask(__name__, template_folder = template_directory)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        destination_folder = request.form['destination']

        html = fetch_html(url)
        if html:
            img_urls = parse_images(html, url)
            download_images (img_urls, destination_folder)
            return f'Images downloaded to {destination_folder}'
        else:
            return 'Failed to retrieve the webpage. Plese check the URL & try again'
        
    return render_template ('index.html')

if __name__ == '__main__':
    app.run(debug = True)