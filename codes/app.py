import os
import sys
from flask import Flask, request, render_template, Response
from time import sleep

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from codes.scraping_logics import scrape_images

# Specify custom template directory
#template_directory = os.path.abspath ("D:/Projects/Data Scraping Application/templates")
template_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')

app = Flask(__name__, template_folder = template_directory)

# Define the route for the homepage
@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':

        # Get the URL and destination folder from the form
        url = request.form.get('url')
        destination_folder = request.form.get('destination')

        # Validate user inputs
        if not url or not destination_folder:
            return 'Both URL and destination folder are required.', 400
        
        # Start scraping process
        try:
            # Launch the image scraping function
            scrape_images(url, destination_folder)
            return f'Successfully downloaded images to {destination_folder}'
        except Exception as e:
            return f'Error occurred: {str(e)}', 500

    # Render the HTML form when method is GET
    return render_template('index.html')

# EventSource route to send real-time updates (image count) to frontend
@app.route('/scrape-stream')
def scrape_stream():
    def generate():
        # Here we simulate image downloading and counting for demonstration
        count = 0
        while count < 10:  # Example: simulating 10 images
            count += 1
            yield f"data: {count}\n\n"
            sleep(1)  # Wait for 1 second before sending the next update
        
        # End the event stream once the process is done
        yield "data: complete\n\n"

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug = False)

