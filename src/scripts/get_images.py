import os
import requests

dog_pic_dir = os.getcwd() + '/dog_pics/'


def _json_to_list_of_urls(json):
  # When querying for a random image from dog.ceo, extract the URLs of the images and return it in a list form
  return json['message']


def get_random_dog_images(quantity=20):
  # Get random images from dog.ceo API
  # This can be used as an input in a trained neural network
  """ Gets random dog images using a GET request.
  kw args: quantity -- amount of random images to get
  returns: a list containing URL(s) that contain .jpg(s) of dog photos.
  """
  url_string = 'https://dog.ceo/api/breeds/image/random/' + str(quantity)
  images = requests.get(url_string)
  image_list = _json_to_list_of_urls(images)
  return image_list


def get_dog_breed_random_images(breed, quantity):
  url_string = 'https://dog.ceo/api/breed/{breed}/images/random/{quantity}'.format(breed=breed, quantity=quantity)
  images = requests.get(url_string)
  image_list = _json_to_list_of_urls(images.json())
  return image_list


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
)