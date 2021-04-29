import os
import json

from tensorflow import keras
from PIL import Image
import numpy as np

from .data_utils import pad_images_black_border, downscale_image, process_all_images_to_fit, split_dataset, prepare_image

def main():
    # Get file path of dog pics dataset.
    dirname = os.getcwd()
    filepath = os.path.join(dirname, 'dog_pics/')

    # Pre-process these by making sure all photos will fit CNN with regards to image dimensions.
    # Comment out this function once pre-processing of dataset is complete.
    process_all_images_to_fit(filepath)
    split_dataset(0.8)

    # image = downscale_image(os.path.join(filepath, 'n02085620-Chihuahua/n02085620_199.jpg'))
    # image = prepare_image(os.path.join(filepath, 'n02085620-Chihuahua/n02085620_7.jpg'))


def make_prediction():
  dirname = os.getcwd()
  filepath = os.path.join(dirname, 'dog_pics/')
  model = keras.models.load_model(
      os.getcwd() + '/src/model/dog_model', compile=False)
  image = prepare_image(os.path.join(filepath, 'n02096585-Boston_bull/n02096585_19.jpg'))
  prediction = model.predict(np.expand_dims(image,axis=0))
  prediction_classes = prediction.argmax(axis=-1)
  print(prediction_classes)

if __name__ == '__main__':
    make_prediction()
    # main()
