import os
import stat
import shutil

if os.name == 'nt':
    import win32api
    import win32con

import cv2
import numpy as np
from sklearn.model_selection import train_test_split

import constants

DOG_PIC_DIR = os.getcwd() + '/augmented_dog_pics/'


def pad_images_black_border(image, dir):
  BLACK = [0, 0, 0]
  img = cv2.imread(image)
  height, width = img.shape[:2]

  offset_height = (constants.IMAGE_HEIGHT - height) // 2
  offset_width = (constants.IMAGE_WIDTH - width) // 2

  padded_image = cv2.copyMakeBorder(
      img, offset_height, offset_height, offset_width, offset_width, cv2.BORDER_CONSTANT, value=BLACK
  )

  if dir is None:
    return padded_image
  elif dir:
    # Save augmented image into an augmented pics folder
    file_name = 'aug_' + os.path.basename(image)
    if not cv2.imwrite(dir + '/' + file_name, padded_image):
      raise Exception("Could not write image")


def downscale_image(image, dir):
  pass
  

def prepare_image(image, dir=None):
  # Does not save it to a directory if dir is None.
  ### Flask --> post request --> saves image to a local path on disk --> use that path to get the image --> process --> predict --> discard/delete image
  img = cv2.imread(image)
  height, width = img.shape[:2]
  processed_image = None

  if height > constants.IMAGE_HEIGHT or width > constants.IMAGE_WIDTH:
    processed_image = downscale_image(image, dir)
  if height <= constants.IMAGE_HEIGHT or width <= constants.IMAGE_WIDTH:
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
      training_set, validation_set = train_test_split(data, train_size=training_split)

      # Move files into a training dataset directory.
      training_dog_breed_dir = dir + 'training_set/' + dog_breeds + '/'
      validation_dog_breed_dir = dir + 'validation_set/' + dog_breeds + '/'

      make_path(training_dog_breed_dir)
      make_path(validation_dog_breed_dir)

      for file in training_set:
        shutil.move(os.path.join(dir, dog_breeds + '/' + file), training_dog_breed_dir)
      for file in validation_set:
        shutil.move(os.path.join(dir, dog_breeds + '/' + file), validation_dog_breed_dir)
      os.rmdir(os.path.join(dir, dog_breeds))
