from flask import Flask, render_template, request, jsonify
import random
import hashlib
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# In-memory dictionary to store predictions based on image hash
image_predictions = {}


# Function to generate hash for the uploaded image
def get_image_hash(file):
    # Read the image file and generate SHA256 hash
    file_content = file.read()
    return hashlib.sha256(file_content).hexdigest()


# Route for the home page
@app.route('/')
def home():
    print("Home route accessed")
    return render_template('home.html')


# Route for the about page
@app.route('/about')
def about():
    print("About route accessed")
    return render_template('about.html')


# Route for the model page
@app.route('/model')
def model():
    return send_file('plant_disease_detection_complete.html')


# Route for the inference page
@app.route('/inference', methods=['GET', 'POST'])
def inference():
    if request.method == 'POST':
        # Handle image file upload
        if 'image' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Generate a hash for the image
        image_hash = get_image_hash(file)

        # Check if the image has been processed before
        if image_hash in image_predictions:
            predicted_class = image_predictions[image_hash]
        else:
            # If the image is new, generate a random predicted class
            predicted_class = random.randint(1, 1000)
            # Store the prediction with the image hash
            image_predictions[image_hash] = predicted_class

        # Return the predicted class (simulated for now)
        return render_template('inference.html', predicted_class=predicted_class)

    # If GET request, just render the inference page with no prediction
    return render_template('inference.html')


if __name__ == '__main__':
    app.run(debug=True)
