from flask import Blueprint, render_template, request, redirect, session, url_for, current_app as app
from werkzeug.utils import secure_filename
import numpy as np
from tensorflow import keras

import os
import json
import re
import threading
import sched
import time

from .forms import FileUploadForm
from ..data_utils import prepare_image, recursive_remove_files
from ..get_images import get_random_image_of_dog_breed, get_wikipedia_entry_of_dog_breed


# Constants
model = None
dog_map = os.getcwd() + '/src/dogs.json'  # Directory of dog map json file


# Blueprint Configuration
bp = Blueprint(
    'bp', __name__,
    # Not actually static, just an easy way of storing/accessing files via blueprints
    static_folder='temp'
)


@bp.before_app_first_request
def load_model():
    global model
    model = keras.models.load_model(
        os.getcwd() + '/src/model/dog_model', compile=False)
    print("Model loaded.")


@bp.route("/", methods=['GET', 'POST'])
def index():
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
        prediction = model.predict(np.expand_dims(
            prepare_image(image_file), axis=0))
        predicted_class_key = np.array2string(prediction.argmax(axis=-1))
        top_5_predictions = np.ndarray.tolist(np.argsort(prediction, axis=1)[:,-5:])[0] # Finish this
        predicted_class_key = re.sub("[^0-9]", "", predicted_class_key)

        # Map the predicted class group to the dog breed label to make it human readable
        with open(dog_map) as fp:
            mapping = json.load(fp)
            class_entry = mapping.get(predicted_class_key)
        session['predicted_class'] = class_entry

        return redirect(url_for("bp.updog"))
    return render_template('index.html', form=form)


@bp.route("/updog", methods=['GET'])
def updog():
    # Extract image and label from sessions
    image = session['image']
    predicted_class = session['predicted_class']

    # Make an API call to dog.ceo to get a random image of the predicted dog breed to display to user
    predicted_dog = get_random_image_of_dog_breed(
        predicted_class['dog_api'].lower())

    # Omit JSON specific regex to make label more human readable
    predicted_class_label = predicted_class['wikipedia'].replace("_", " ").replace("-", "")

    # Get wikipedia entry URL for dog breed to load into iFrame in template
    wiki_dog = get_wikipedia_entry_of_dog_breed(predicted_class['wikipedia'])

    # Create instance of scheduler to delete uploaded photo once served to the html page as they will no longer be needed
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(10, 1, recursive_remove_files,
                    (bp.static_folder, 'README.md'))

    # Ran inside a spwaned instance of a thread to provide concurrency and non-blocking execution
    delete_thread = threading.Thread(target=scheduler.run)
    delete_thread.start()
    return render_template('updog.html',
                           image=image,
                           predicted_class_label=predicted_class_label,
                           predicted_dog=predicted_dog,
                           wiki_entry=wiki_dog)


@bp.route("/motivation")
def about():
    return render_template('motivation.html')
