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

def get_dog_breed_image(breed):
  pass

def json_to_serializable_format(json_images):
  pass

