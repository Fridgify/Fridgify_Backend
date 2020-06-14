from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '[::1]',
    "fridgapi.donkz.dev",
    "api.fridgify.com"
]

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


CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    'http://localhost',
    'http://127.0.0.1'
]
