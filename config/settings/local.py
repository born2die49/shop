from os import getenv, path

from dotenv import load_dotenv

from .base import * #noqa

from .base import BASE_DIR

local_env_file = path.join(BASE_DIR, ".envs", ".env.local")

if path.isfile(local_env_file):
  load_dotenv(local_env_file)
  
DEBUG = True

SITE_NAME = getenv("SITE_NAME")

SECRET_KEY = getenv("DJANGO_SECRET_KEY", "-O6-UyEOl88jGQdndiMSGJo4NgZ5zeMpCDUgwF9JQ4Uezx2rxMQ")

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

ADMIN_URL = getenv("DJANGO_ADMIN_URL")

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = getenv("EMAIL_HOST")
EMAIL_PORT = getenv("EMAIL_PORT")
DEFAULT_FORM_EMAIL = getenv("DEFAULT_FORM_EMAIL")
DOMAIN = getenv("DOMAIN")