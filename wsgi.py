import os
from tensorflow import keras
from src.web_app import init_app

model = None
app = init_app()


def load_model():
    global model
    model = keras.models.load_model(
        os.getcwd() + '/src/model/dog_model', compile=False)
    print("Model loaded.")


if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))
    load_model()
    app.debug = True
    app.run()
