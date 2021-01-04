import get_images as dbc_images

###TODO: check for correct dimensions --> if no --> pad image with black border to correct dimension
###                                   \--> if yes --> feed into CNN

def is_correct_dimensions(image):
  """
  Checks if the image has the correct dimensions to be able to be fed into the CNN properly.
  args: image -- (string) directory of image.
  returns: (boolean) -- True or False, if image has correct dimensions.
  """
  return False

def pad_images_for_correct_dimensions(image):
  pass

def resize_image_with_same_aspect_ratio(image_src):
  """
  Upscales or downscales image if it can fit within the same aspect ratio.
  This makes it so that the image is valid to be fed into the CNN.
  """
  pass

def json_to_serializable_format(json_images):
  pass

