from config.settings import *

DEBUG = True

SECRET_KEY = 'django-insecure-sb!$c)o$c9!zdf+h%a)crg8*wqsu83bl!hj9ql7w4zg=n(sibc'

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

WSGI_APPLICATION = 'config.wsgi.develop.application'

STATIC_URL = 'static/'
