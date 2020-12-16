"""
Sabra George and Melissa Mullen Group Implementation Project
December 17, 2020
COMP 740
"""

import os
import base64
import random
import cv2
import googleapiclient.discovery
import tensorflow as tf
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from google.api_core.client_options import ClientOptions

# Initialise Flask
app = Flask(__name__)

# Provide credentials to authenticate to a Google Cloud API
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'aikey.json'

# Temporary storage for uploaded pictures
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Image extension allowed
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def upload_file():
    """
    This function allows the user to upload a file.

    Returns:
        filepath: uploaded picture.
        prediction_results: array of prediction results (floats)
            defined by the model.
        pred_look (string): probability of looking at screen.
        pred_away (string): probability of looking away from screen.
    """
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            prediction_results, pred_look, pred_away = search(filepath)
            return render_template(
                'search_results.html',
                original=filepath,
                prediction_results=prediction_results,
                pred_look=pred_look,
                pred_away=pred_away
            )


@app.route('/camera')
def camera():
    """
    This function opens your webcam, takes a picture when you hit the space bar
    and sends the picture to the predictive model

    Returns:
        image: picture taken on your webcam (png file)
        prediction_results: array of prediction results (floats)
            defined by the model.
        pred_look (string): probability of looking at screen.
        pred_away (string): probability of looking away from screen.
    """

    camera = cv2.VideoCapture(0)
    cv2.namedWindow("Model Camera")
    number = random.randint(0, 999)   # for naming images

    while True:
        ret, frame = camera.read()
        # if the camera cannot launch, return an error png
        if not ret:
            print("Failed to launch camera")
            image = "static/error.png"
            break

        cv2.imshow("Model Camera", frame)

        key = cv2.waitKey(1)
        if key%256 == 27:   # ESC pressed
            # If escape is pressed, close camera and return an error png
            print("Escape hit, closing camera")
            image = "static/error.png"
            break

        elif key%256 == 32:
            # SPACE pressed
            # Take picture and save it
            image = "static/captured_image_{}.png".format(number)
            cv2.imwrite(image, frame)
            print("{} written!".format(image))
            print("Image captured, closing camera")
            break

    camera.release()   # close camera
    cv2.destroyAllWindows()   # destroy all windows the camera opened

    prediction_results, pred_look, pred_away = search(image)
    return render_template(
        'search_results.html',
        original=image,
        prediction_results=prediction_results,
        pred_look=pred_look,
        pred_away=pred_away
    )

def search(f):
    '''
    This function takes the image that the user either submits or takes, converts
    it into binary code, and send the code to the specific AI Platform Image
    Classification Model. This will then return probability for each class.
    '''
    #convert image to binary encoded string for the model to read
    with open(f, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    image_bytes = {'b64': str(encoded_string)}
    instances = [{'image_bytes': image_bytes, 'key': '1'}]
    
    #establishing varibales for calling model
    project = "aitry-294619"
    region = "us-central1"
    model = "trial41"
    version = "v1"

    #creating the api endpoint from model variables
    prefix = "{}-ml".format(region) if region else "ml"
    api_endpoint = "https://{}.googleapis.com".format(prefix)
    client_options = ClientOptions(api_endpoint=api_endpoint)
    service = googleapiclient.discovery.build(
        'ml', 'v1', client_options=client_options)
    name = 'projects/{}/models/{}'.format(project, model)

    if version is not None:
        name += '/versions/{}'.format(version)
    
    #sending the image to the model for running
    response = service.projects().predict(
        name=name,
        body={'instances': instances}
    ).execute()

    if 'error' in response:
        raise RuntimeError(response['error'])
        
    #return results as a percentage
    prediction_results = response['predictions'][0]['probabilities']
    pred_look = str(prediction_results[0] * 100) + "%"
    pred_away = str(prediction_results[1] * 100) + "%"

    return prediction_results, pred_look, pred_away


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
