from flask import Blueprint, render_template, redirect, session, url_for, current_app as app
from werkzeug.utils import secure_filename
import os

from .forms import FileUploadForm

# Blueprint Configuration
bp = Blueprint(
    'bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@bp.route("/", methods=['GET', 'POST'])
def index():
    # Upload dog image -- for uploading a file that contains an image (presumably, of a dog)
    form = FileUploadForm()
    if form.validate_on_submit():
        file_name = secure_filename(form.file.data.filename)
        form.file.data.save(bp.static_folder + '/' + file_name)
        session['image'] = file_name
        # 1. Predict here and then save it in a session.
        return redirect(url_for("bp.updog"))
    return render_template('index.html', form=form)


@bp.route("/updog", methods=['GET'])
def updog():
    # 2. Extract the prediction from the session and pass it into the template to render too.
    # 3. Write a callback to delete the files and execute in the template
    image = session['image']
    return render_template('updog.html', image=image)


@bp.route("/motivation")
def about():
    return render_template('motivation.html')
