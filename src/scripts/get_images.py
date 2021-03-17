# Get random images from dog.ceo API
# This can be used as an input in a trained neural network
import os
import requests

dog_pic_dir = os.getcwd() + '/dog_pics/'

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
  args: image_url -- (string) URL with what we think is an image.
  returns: (boolean) -- True OR False, if url contains a valid image.
  """
  valid_formats = ("image/png", "image/jpeg", "image/jpg")
  r = requests.get(image_url)
  if r.headers["content-type"] in valid_formats:
      return True
  return False


def check_dir_contains_valid_image(image_src):
  """
  Checks if an file from a local directory is a valid image.
  args: image_src -- (string) directory of file
  returns: (boolean) -- True OR False, if file is a valid image.
  """
  pass

def save_image_locally(url, dir):
  """
  Gets image file from URL and saves it into a directory with the base name of the file as it is. (Checks if image first)
  args:
    url -- (string) URL of file
    dir -- (string) target directory where file is saved
  """
  if check_url_contains_valid_image(url):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
      file_name = os.path.basename(url)
      with open(dir + file_name, 'wb') as f:
        for chunk in r:
          f.write(chunk)
