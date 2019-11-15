from .base import *

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', "fridgapi.donkz.dev"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'backend_test',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'db_test',
        'PORT': '5432',
    }
}