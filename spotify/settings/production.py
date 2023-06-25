from .base import *

DEBUG = False


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'spotify',
        'USER': 'postgres',
        'PASSWORD': '1111',
        'HOST': '35.202.13.40',  # Typically 'localhost' if running locally
    }
}