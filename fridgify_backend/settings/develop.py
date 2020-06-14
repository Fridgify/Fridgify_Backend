from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '[::1]',
    "fridgapi-dev.donkz.dev",
    "api-dev.fridgify.com"
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'backend_develop',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'db_develop',
        'PORT': '5432',
    }
}

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    "https://dev.fridgify.com",
]
