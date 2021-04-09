import flask
import os
from tensorflow import keras

app = flask.Flask(__name__)
model = None


def load_model():
    global model
    model = keras.models.load_model(os.getcwd() + '/src/model/dog_model', compile=False)
    print("Model loaded.")


@app.route("/updog", methods=["POST"])
def predict()
    pass


if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
        "please wait until server has fully started"))
    load_model()
    app.run()
