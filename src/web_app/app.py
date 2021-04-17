from flask import Flask, render_template
import os
from tensorflow import keras

application = Flask(__name__)
model = None


### Model
def load_model():
    global model
    model = keras.models.load_model(
        os.getcwd() + '/src/model/dog_model', compile=False)
    print("Model loaded.")


### Routes
@application.route("/")
def landing():
    return render_template('index.html')

@application.route("/motivation")
def about():
    return render_template('motivation.html')

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
