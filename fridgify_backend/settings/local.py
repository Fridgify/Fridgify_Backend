from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', "fridgapi.donkz.dev"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'backend_test.sqlite',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'db_test',
        'PORT': '5432',
    }
}
