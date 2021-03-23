import os, stat

if os.name == 'nt':
    import win32api, win32con

import cv2
import numpy as np

import constants

DOG_PIC_DIR = os.getcwd() + '/augmented_dog_pics/'

def pad_images_black_border(image, dir):
  """ Pads an image with a black border so that it conforms to the dimensions needed for the CNN.
    It then writes and saves it in a folder.
  kw args: image -- a string file path that should contain an image.
  returns: None
  """
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
  file_name = 'aug_' + os.path.basename(image)
  if not cv2.imwrite(dir + '/' + file_name, padded_image):
     raise Exception("Could not write image")


def process_all_images_to_fit(dir):
  # Custom script -- should take the stanford dogs dataset directory and folders/files and either:
  #     - save the files to DOG_PIC_DIR if there is no need for augmentation for dimensions to fit CNN
  #     - augment the photos first and then save the files to DOG_PIC_DIR
  for root, folders, files in os.walk(dir):
    for dog_breeds in folders:
      if not os.path.exists(DOG_PIC_DIR + dog_breeds):
        os.makedirs(DOG_PIC_DIR + dog_breeds)
    for name in files:
      # If hidden file is detected, skip iteration.
      if is_hidden_file(name):
        continue
      pad_images_black_border(os.path.join(root, name),
                              DOG_PIC_DIR + os.path.basename(root))


def is_hidden_file(filepath):
    if os.name== 'nt':
        attribute = win32api.GetFileAttributes(filepath)
        return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    else:
        return filepath.startswith('.') #linux-osx
