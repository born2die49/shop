from pathlib import Path
from os import getenv, path

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

APPS_DIR = BASE_DIR / "core_apps"

local_env_file = path.join(BASE_DIR, ".envs", ".env.local")

if path.isfile(local_env_file):
  load_dotenv(local_env_file)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites'
]

THIRD_PARTY_APPS = [
  "rest_framework",
  "django_countries",
  "phonenumber_field",
  "djoser",
  "taggit",
  "drf_yasg",
  "social_django",
  "django_filters",
  "djcelery_email",
  "django_celery_beat",
  "storages"
]

LOCAL_APPS = [
    "core_apps.user",
    "core_apps.common",
    "core_apps.profiles",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(APPS_DIR / "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv("POSTGRES_DB"),
        'USER': getenv("POSTGRES_USER"),
        'PASSWORD': getenv("POSTGRES_PASSWORD"),
        'HOST': getenv("POSTGRES_HOST"),
        'PORT': getenv("POSTGRES_PORT"),
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True

SITE_ID = 1


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = str(BASE_DIR / "staticfiles")

TAGGIT_CASE_INSENSITIVE = True

AUTH_USER_MODEL = "user.User"

if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE
    
CELERY_BROKER_URL = getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = getenv("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULTS_SERIALIZER = 'json'
CELERY_RESULTS_BACKEND_MAX_RETRIES = 10

CELERY_TASK_SEND_SENT_EVENT = True
CELERY_RESULT_EXTENDED = True

CELERY_RESULT_BACKEND_ALWAYS_RETRY = True

CELERY_TASK_TIME_LIMIT = 5*60

CELERY_TASK_SOFT_TIME_LIMIT = 60

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

CELERY_WORKER_SEND_TASK_EVENTS = True

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = getenv("AWS_S3_REGION_NAME", "us-east-1")

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None 
AWS_S3_VERIFY = True

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# Media Files (User uploads) to S3
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# URL configuration to read files from s3
MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/"