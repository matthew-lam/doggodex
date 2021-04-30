from flask import Blueprint, render_template, request, redirect, session, url_for, current_app as app
from werkzeug.utils import secure_filename
import numpy as np
from tensorflow import keras

import os
import json
import re

from .forms import FileUploadForm
from ..data_utils import prepare_image, scale
from ..get_images import get_random_image_of_dog_breed


# Blueprint Configuration
bp = Blueprint(
    'bp', __name__,
    static_folder='static' # Not actually static, just an easy way of storing/accessing files via blueprints
)

model = None
dog_map = os.getcwd() + '/src/dogs.json' # Directory of dog map json file

@bp.before_app_first_request
def load_model():
    global model
    model = keras.models.load_model(
        os.getcwd() + '/src/model/dog_model', compile=False)
    print("Model loaded.")


@bp.route("/", methods=['GET', 'POST'])
def index():
    # Ensures that folder holding images is empty first.
    for file in os.scandir(bp.static_folder):
        os.unlink(file)

    # Setup for predicted class label
    label = None
    # Render form and ensure that a valid file is submitted
    form = FileUploadForm()
    if form.validate_on_submit():
        # Save image to 'static' folder for rendering into template
        file_name = secure_filename(form.file.data.filename)
        image_file = bp.static_folder + '/' + file_name
        form.file.data.save(image_file)
        session['image'] = file_name
        # Make a prediction out of the submitted image
        prediction = model.predict(np.expand_dims(prepare_image(image_file), axis=0))
        predicted_class = np.array2string(prediction.argmax(axis=-1))
        predicted_class = int(re.sub("[^0-9]", "", predicted_class))
        # Map the predicted class group to the dog breed label to make it human readable
        with open(dog_map) as fp:
            mapping = json.load(fp)
            label = list(mapping.keys())[list(mapping.values()).index(predicted_class)]
        session['predicted_class_label'] = label.partition("-")[2].capitalize()
        return redirect(url_for("bp.updog"))
    return render_template('index.html', form=form)


@bp.route("/updog", methods=['GET'])
def updog():
    # Extract image and label from sessions
    image = session['image']
    predicted_class_label = session['predicted_class_label']
    # Make an API call to dog.ceo to get a random image of the predicted dog breed to display to user
    predicted_dog = get_random_image_of_dog_breed(
        predicted_class_label.lower())
    return render_template('updog.html',
                           image=image,
                           predicted_class_label=predicted_class_label.replace(
                               "_", " ").replace("(", "").replace(")", ""),
                           predicted_dog=predicted_dog)


@bp.route("/motivation")
def about():
    return render_template('motivation.html')
