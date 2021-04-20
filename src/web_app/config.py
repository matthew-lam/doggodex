from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    DEBUG = True
    SECRET_KEY = environ.get("SECRET_KEY")
    RECAPTCHA_PUBLIC_KEY = environ.get("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = environ.get("RECAPTCHA_PRIVATE_KEY")
    RECAPTCHA_USE_SSL = False
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB

