import flask
import os
from tensorflow import keras

application = flask.Flask(__name__)
model = None


def load_model():
    global model
    model = keras.models.load_model(os.getcwd() + '/src/model/dog_model', compile=False)
    print("Model loaded.")


@application.route("/updog")
def predict():
    print('testing -- it works!!')
    return ('hello world')


if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
        "please wait until server has fully started"))
    load_model()
    application.debug = True
    application.run()
