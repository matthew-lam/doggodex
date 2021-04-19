from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField

error_messages = {
    "format_error": "File is of the wrong format -- please use jpg, png or bmp.",
    "no_file": "No file detected for upload."
}


class FileUploadForm(FlaskForm):
    file = FileField(label='image', validators=[FileAllowed(
        ['jpeg', 'jpg', 'png', 'bmp'], error_messages['format_error']), FileRequired(error_messages['no_file'])])
    recaptcha = RecaptchaField()
    submit = SubmitField('Upload')

# Secure file names
# Max image size
# Set HTML form enctype to multipart/form-data otherwise request.files will be empty