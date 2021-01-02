# Get random images from dog.ceo API
# This can be used as an input in a trained neural network

import requests

def get_random_dog_images(quantity=20):
  """ Gets random dog images using a GET request.
  kw args: quantity -- amount of random images to get
  returns: a JSON containing a message array of URL(s) that contain .jpg(s) of dog photos.
  """
  url_string = 'https://dog.ceo/api/breeds/image/random/' + str(quantity)
  images = requests.get(url_string)
  return images

def check_url_contains_valid_image(image_url):
  """
  Checks if a url has a valid image.
  It does this by checking the media type in the header of the http request response.
  args: image_url -- URL with what we think is an image.
  returns: (boolean) -- True OR False, if url contains a valid image.
  """
  valid_formats = ("image/png", "image/jpeg", "image/jpg")
  url_contents = requests.get(image_url)
  if url_contents.headers["content-type"] in valid_formats:
      return True
  return False


def check_dir_contains_valid_image(image_src):
  pass
