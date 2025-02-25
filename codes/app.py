import os
import sys
from flask import Flask, request, render_template, Response, jsonify
from time import sleep

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from codes.scraping_logics import scrape_images

# Specify custom template directory
#template_directory = os.path.abspath ("D:/Projects/Data Scraping Application/templates")
#template_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')

app = Flask(__name__)

# Define the route for the homepage
@app.route('/api/scrape', methods=['POST'])

def scrape_api():
    # Get data from the request (URL and destination folder)
    data = request.get_json()
    url = data.get('url')
    destination_folder = data.get('destination')

    # Validate inputs
    if not url or not destination_folder:
        return jsonify({'error': 'Both URL and destination folder are required.'}), 400
    
    # Start scraping process
    try:
        scrape_images(url, destination_folder)
        return jsonify({'message': f'Successfully downloaded images to {destination_folder}'}), 200
    except Exception as e:
        return jsonify({'error': f'Error occurred: {str(e)}'}), 500

# EventSource route to send real-time updates (image count) to frontend
@app.route('/api/scrape-stream', methods=['GET'])
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
    