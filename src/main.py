import os
import json


from tensorflow import keras
from PIL import Image
import numpy as np

from .data_utils import pad_images_black_border, downscale_image, process_all_images_to_fit, split_dataset, prepare_image
from .get_images import get_random_image_of_dog_breed, get_wikipedia_entry_of_dog_breed

dog_map = os.getcwd() + '/src/dogs.json'  # Directory of dog map json file


def main():
    # Get file path of dog pics dataset.
    dirname = os.getcwd()
    filepath = os.path.join(dirname, 'dog_pics/')

    # Pre-process these by making sure all photos will fit CNN with regards to image dimensions.
    # Comment out this function once pre-processing of dataset is complete.
    process_all_images_to_fit(filepath)
    split_dataset(0.8)


def get_dog():
    predicted_class = "0"
    with open(dog_map) as fp:
        mapping = json.load(fp)
        label = mapping.get(predicted_class)['wikipedia']
    print(label)

def sort_dict():
    with open(dog_map, 'r+') as fp:
        mapping = json.load(fp)
        for k, v in mapping.items():
            dog = { "wikipedia_suffix": v, "dog_api_suffix": v }
            mapping[k] = dog
        dump = json.dumps(mapping)
        fp.write(dump)


if __name__ == '__main__':
    # sort_dict()
    # get_dog()
    # main()
