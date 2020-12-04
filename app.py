import os
import json
import base64
import tensorflow as tf
# import googleapiclient.discovery
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from googleapiclient import discovery
from googleapiclient import errors
from google.api_core.client_options import ClientOptions

# Initialise Flask
app = Flask(__name__)

# Provide credentials to authenticate to a Google Cloud API
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'aikey.json'

# Temporary storage for uploaded pictures
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Maximum Image Uploading size
# app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

# Image extension allowed
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def upload_file():
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
    """
    import cv2
    import random

    camera = cv2.VideoCapture(0)
    cv2.namedWindow("Model Camera")
    number = random.randint(0, 999)

    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to launch camera")
            image = "static/error.png"
            break

        cv2.imshow("Model Camera", frame)

        key = cv2.waitKey(1)
        if key%256 == 27:
            # ESC pressed
            print("Escape hit, closing camera")
            break

        elif key%256 == 32:
            # SPACE pressed
            image = "static/captured_image_{}.png".format(number)
            cv2.imwrite(image, frame)
            print("{} written!".format(image))
            print("Image captured, closing camera")
            break

    camera.release()
    cv2.destroyAllWindows()

    prediction_results, pred_look, pred_away = search(image)
    return render_template(
        'search_results.html',
        original=image,
        prediction_results=prediction_results,
        pred_look=pred_look,
        pred_away=pred_away
    )


def search(f):
    with open(f, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    image_bytes = {'b64': str(encoded_string)}
    instances = [{'image_bytes': image_bytes, 'key': '1'}]

    """
    Send json data to a deployed model for prediction.

    Args:
        project (str): project where the Cloud ML Engine Model is deployed.
        region (str): regional endpoint to use; set to None for
        ml.googleapis.com
        model (str): model name.
        instances ([Mapping[str: Any]]): Keys should be the names of Tensors
            your deployed model expects as inputs. Values should be datatypes
    #         convertible to Tensors, or (potentially nested) lists of
    #         datatypes convertible to tensors.
    #     version: str, version of the model to target.
    # Returns:
    #     Mapping[str: any]: dictionary of prediction results defined by the
            model.
    # """
    project = "aitry-294619"
    region = "us-central1"
    model = "Model_3"
    version = "v1"
    # Create the ML Engine service object.
    # To authenticate set the environment variable
    # GOOGLE_APPLICATION_CREDENTIALS= '/Users/sabrageorge/Local Documents/
    #   Capstone/full_project/aikey.json'
    prefix = "{}-ml".format(region) if region else "ml"
    api_endpoint = "https://{}.googleapis.com".format(prefix)
    client_options = ClientOptions(api_endpoint=api_endpoint)
    service = googleapiclient.discovery.build(
        'ml', 'v1', client_options=client_options)
    name = 'projects/{}/models/{}'.format(project, model)

    if version is not None:
        name += '/versions/{}'.format(version)

    # instances = open('prediction_instances.json', 'r')

    response = service.projects().predict(
        name=name,
        body={'instances': instances}
    ).execute()

    if 'error' in response:
        raise RuntimeError(response['error'])

    prediction_results = response['predictions'][0]['probabilities']
    pred_look = prediction_results[0]
    pred_away = prediction_results[1]

    return prediction_results, pred_look, pred_away

    # if response.error.message:
        # raise Exception(
            # '{}\nFor more info on error messages, check: '
            # 'https://cloud.google.com/apis/design/errors'.format(
                # response.error.message))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
