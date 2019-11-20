from .base import *

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', "fridgapi.donkz.dev"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'backend',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'db',
        'PORT': '5432',
    }
}
