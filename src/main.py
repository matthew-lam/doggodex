import os
from scripts.data_utils import pad_images_black_border, process_all_images_to_fit
from scripts.get_images import get_dog_breed_random_images, save_image_locally
from model.conv_net import run_model

def main():
    # Get file path of dog pics dataset.
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, '../dog_pics/')

    # Pre-process these by making sure all photos will fit CNN with regards to image dimensions.
    # Comment out this function once pre-processing of dataset is complete.
    process_all_images_to_fit(filepath)

    # run_model()


if __name__ == '__main__':
    main()
