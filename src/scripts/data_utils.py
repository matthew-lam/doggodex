import os

import cv2
import numpy as np

import get_images as dbc_images
from ..constants import image_HEIGHT, image_WIDTH

###TODO: check for correct dimensions --> if no --> pad image with black border to correct dimension
###                                   \--> if yes --> feed into CNN

dog_pic_dir = os.getcwd() + '/augmented_dog_pics/'

def is_correct_dimensions(image):
  """
  Checks if the image has the correct dimensions to be able to be fed into the CNN properly.
  args: image -- (string) directory of image.
  returns: (boolean) -- True or False, if image has correct dimensions.
  """
  return False

def pad_images_black_border(image):
  file_name = os.path.basename(image)
  img = cv2.imread(image)

  height, width, channels = img.shape
  border_color = (0, 0, 0) # black

  output = np.full((image_HEIGHT, image_WIDTH, channels), border_color, dtype=np.uint8)

  # compute offsets
  xx = (image_WIDTH - width) // 2
  yy = (image_HEIGHT - height) // 2

  # copy img image into center of result image
  output[yy: yy + height, xx: xx + width] = img

  # save augmented image into an augmented pics folder
  cv2.imwrite(dog_pic_dir + file_name, output)



def resize_image_with_same_aspect_ratio(image_src):
  """
  Upscales or downscales image if it can fit within the same aspect ratio.
  This makes it so that the image is valid to be fed into the CNN.
  """
  pass

def json_to_serializable_format(json_images):
  pass

def main():
  pad_images_black_border('../../dog_pics/n02112137_1251.jpg')

if __name__ == '__main__':
    main()
