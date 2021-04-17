from flask import Blueprint, render_template
from flask import current_app as app


# Blueprint Configuration
bp = Blueprint(
    'bp', __name__,
    template_folder='templates',
)


# Routes
@bp.route("/")
def landing():
    return render_template('index.html')


@bp.route("/motivation")
def about():
    return render_template('motivation.html')


@bp.route("/updog")
def predict():
    print('testing -- it works!!')
    return ('hello world')
