from flask import Blueprint, render_template, redirect, request, session, url_for, current_app as app
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
        return redirect(url_for("bp.updog"))
    return render_template('index.html', form=form)


@bp.route("/updog", methods=['GET'])
def updog():
    return render_template('updog.html')


@bp.route("/motivation")
def about():
    return render_template('motivation.html')
