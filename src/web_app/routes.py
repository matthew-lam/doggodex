from flask import Blueprint, render_template, request, redirect, session, url_for, current_app as app
from werkzeug.utils import secure_filename
import numpy as np

import os

from .forms import FileUploadForm
from .scripts.data_utils import prepare_image

# Blueprint Configuration
bp = Blueprint(
    'bp', __name__,
    static_folder='static' # Not actually static, just an easy way of storing/accessing files via blueprints
)

@bp.route("/", methods=['GET', 'POST'])
def index():
    # Ensures that folder holding images is empty first.
    for file in os.scandir(bp.static_folder):
        os.unlink(file)

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
        predicted_class = prediction.argmax(axis=-1)
        session['predicted_class'] = predicted_class
        return redirect(url_for("bp.updog"))
    return render_template('index.html', form=form)


@bp.route("/updog", methods=['GET'])
def updog():
    # 2. Extract the prediction from the session and pass it into the template to render too.
    # 3. Write a callback to delete the files and execute in the template
    image = session['image']
    predicted_class = session['predicted_class']
    return render_template('updog.html', image=image, predicted_class=predicted_class)


@bp.route("/motivation")
def about():
    return render_template('motivation.html')
