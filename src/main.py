import os
import json

from tensorflow import keras
from PIL import Image
import numpy as np

from .data_utils import process_all_images_to_fit, split_dataset


dog_map = os.getcwd() + '/src/dogs.json'  # Directory of dog map json file


def main():
    # Get file path of dog pics dataset.
    dirname = os.getcwd()
    filepath = os.path.join(dirname, 'dog_pics/')

    # Pre-process these by making sure all photos will fit CNN with regards to image dimensions.
    # Comment out this function once pre-processing of dataset is complete.
    process_all_images_to_fit(filepath)
    split_dataset(0.8)


if __name__ == '__main__':
    # main()
