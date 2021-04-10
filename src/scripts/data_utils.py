import os
import stat
import shutil
import math
import cv2

if os.name == 'nt':
    import win32api
    import win32con

import cv2
import numpy as np
from sklearn.model_selection import train_test_split

import constants

DOG_PIC_DIR = os.getcwd() + '/augmented_dog_pics/'


def pad_images_black_border(image, dir=None):
  # Pad image with a border so that smaller images fit in to the CNN
  BLACK = [0, 0, 0]
  img = cv2.imread(image)
  height, width = img.shape[:2]

  border_height = (constants.IMAGE_HEIGHT - height) / 2
  border_width = (constants.IMAGE_WIDTH - width) / 2

  padded_image = cv2.copyMakeBorder(
      img,
      math.ceil(border_height), math.floor(border_height), math.ceil(
          border_width), math.floor(border_width),
      cv2.BORDER_CONSTANT, value=BLACK
  )

  if dir is None:
    return padded_image
  elif dir:
    # Save augmented image into an augmented pics folder
    file_name = 'aug_' + os.path.basename(image)
    if not cv2.imwrite(dir + '/' + file_name, padded_image):
      raise Exception("Could not write image")


def scale(source, target) -> (int, int):
    width, height = source
    max_width, max_height = target

    # if both width, height is smaller then keep them
    if (width <= max_width) and (height <= max_height):
        return (width, height)
    # if they're both bigger, then scale it down based on whichever is bigger.
    else:
        new_x, new_y = width, height
        if width/max_width >= height/max_height:
            # height is bigger, so that will need to scale to target height.
            new_x = max_width
            new_y = height * (max_width/width)
        else:
            new_x = width * (max_height/height)
            new_y = max_height
        return (int(new_x), int(new_y))


def downscale_image(image, dir=None):
  # Scale down images to retain quality and then pad them with a border to fit into CNN input
  BLACK = [0, 0, 0]
  img = cv2.imread(image)
  height, width = img.shape[:2]

  new_width, new_height = scale((width, height), (constants.IMAGE_WIDTH, constants.IMAGE_HEIGHT))
  border_width = constants.IMAGE_WIDTH - new_width
  border_height = constants.IMAGE_HEIGHT - new_height

  padded_image = cv2.copyMakeBorder(
      img, border_height, 0, border_width, 0, cv2.BORDER_CONSTANT, value=BLACK
  )

  padded_image = cv2.resize(padded_image, (constants.IMAGE_WIDTH,
                                           constants.IMAGE_HEIGHT), interpolation=cv2.INTER_AREA)
  if dir is None:
    return padded_image
  elif dir:
    # Save augmented image into an augmented pics folder
    file_name = 'aug_' + os.path.basename(image)
    if not cv2.imwrite(dir + '/' + file_name, padded_image):
      raise Exception("Could not write image")


def prepare_image(image, dir=None):
  # Does not save it to a directory if dir is None.
  ### Flask --> post request --> saves image to a local path on disk --> use that path to get the image --> process --> predict --> discard/delete image
  img = cv2.imread(image)
  height, width = img.shape[:2]
  processed_image = None

  if height > constants.IMAGE_HEIGHT or width > constants.IMAGE_WIDTH:
    processed_image = downscale_image(image, dir)
  
  if height <= constants.IMAGE_HEIGHT and width <= constants.IMAGE_WIDTH:
    processed_image = pad_images_black_border(image, dir)
  
  return processed_image


def make_path(dir):
  if not os.path.exists(dir):
    os.makedirs(dir)


def process_all_images_to_fit(dir):
  # Custom script -- should take the stanford dogs dataset directory and folders/files and either:
  #     - save the files to DOG_PIC_DIR if there is no need for augmentation for dimensions to fit CNN
  #     - augment the photos first and then save the files to DOG_PIC_DIR
  for root, folders, files in os.walk(dir):
    for dog_breeds in folders:
      make_path(DOG_PIC_DIR + dog_breeds)
    for name in files:
      # If hidden file is detected, skip iteration.
      if is_hidden_file(name):
        continue
      prepare_image(os.path.join(root, name),
                    DOG_PIC_DIR + os.path.basename(root))


def is_hidden_file(filepath):
    if os.name == 'nt':
        attribute = win32api.GetFileAttributes(filepath)
        return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    else:
        return filepath.startswith('.')  # linux-osx


def split_dataset(training_split, dir=DOG_PIC_DIR):
  for _, folders, _ in os.walk(dir):
    for dog_breeds in folders:
      data = os.listdir(os.path.join(dir, dog_breeds))
      training_set, validation_set = train_test_split(
          data, train_size=training_split)

      # Move files into a training dataset directory.
      training_dog_breed_dir = dir + 'training_set/' + dog_breeds + '/'
      validation_dog_breed_dir = dir + 'validation_set/' + dog_breeds + '/'

      make_path(training_dog_breed_dir)
      make_path(validation_dog_breed_dir)

      for file in training_set:
        shutil.move(os.path.join(dir, dog_breeds + '/' + file),
                    training_dog_breed_dir)
      for file in validation_set:
        shutil.move(os.path.join(dir, dog_breeds + '/' + file),
                    validation_dog_breed_dir)
      os.rmdir(os.path.join(dir, dog_breeds))
