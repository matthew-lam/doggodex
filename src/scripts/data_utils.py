import os

import cv2
import numpy as np

import constants

DOG_PIC_DIR = os.getcwd() + '/augmented_dog_pics/aug_'


def pad_images_black_border(image):
  # Pads an image with a black border so that it conforms to the dimensions needed for the CNN.
  BLACK = [0, 0, 0]
  img = cv2.imread(image)
  height, width = img.shape[:2]

  # Only pad images if smaller than certain dimensions
  if height > constants.IMAGE_HEIGHT or width > constants.IMAGE_WIDTH:
    return

  offset_height = (constants.IMAGE_HEIGHT - height) // 2
  offset_width = (constants.IMAGE_WIDTH - width) // 2

  padded_image = cv2.copyMakeBorder(
      img, offset_height, offset_height, offset_width, offset_width, cv2.BORDER_CONSTANT, value=BLACK
  )

  # Save augmented image into an augmented pics folder
  file_name = os.path.basename(image)
  if not cv2.imwrite(DOG_PIC_DIR + file_name, padded_image):
     raise Exception("Could not write image")


def json_to_list_of_urls(json):
  # When querying for a random image from dog.ceo, extract the URLs of the images and return it in a list form
  return json['message']
