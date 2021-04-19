from flask import Blueprint, render_template, redirect, request, url_for, current_app as app
from .forms import FileUploadForm

# Blueprint Configuration
bp = Blueprint(
    'bp', __name__,
    template_folder='templates',
)


@bp.route("/", methods=['GET', 'POST'])
def updog():
    # Upload dog image -- for uploading a file that contains an image (presumably, of a dog)
    upload_form = FileUploadForm()
    # May need to change this to validate_on_submit()
    if upload_form.is_submitted():
        print('Received a validated pic')
    return render_template('index.html', form=upload_form)


@bp.route("/motivation")
def about():
    return render_template('motivation.html')
