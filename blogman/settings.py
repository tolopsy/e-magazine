import os
import dj_database_url
from django.contrib.messages import constants as messages
from dotenv import load_dotenv, find_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['tidings.herokuapp.com', '127.0.0.1']

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'blog.apps.BlogConfig',
    'ckeditor',
    'ckeditor_uploader',
    'taggit',
    'tinymce'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blogman.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blogman.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Google Media Storage Setting
if not DEBUG:
    DEFAULT_FILE_STORAGE = 'gcloud.GoogleCloudMediaFileStorage'
    GS_PROJECT_ID = "your google cloud project id"
    GS_MEDIA_BUCKET_NAME = 'name of your google cloud bucket'

    MEDIA_URL = 'https://storage.googleapis.com/{}/'.format(GS_MEDIA_BUCKET_NAME)
    MEDIA_ROOT = "media/"

    UPLOAD_ROOT = 'media/uploads/'

else:
    MEDIA_URL  = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# DOWNLOAD_ROOT = os.path.join(BASE_DIR, "static/media/downloads")
# DOWNLOAD_URL = MEDIA_URL + "media/downloads"

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('HOST')
EMAIL_HOST_USER = os.getenv('HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_USE_SSL = False

CKEDITOR_UPLOAD_PATH = 'blog-uploads/'