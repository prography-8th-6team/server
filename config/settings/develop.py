from config.settings import *

DEBUG = True

SECRET_KEY = env('DEV_SECRET_KEY')

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

WSGI_APPLICATION = 'config.wsgi.develop.application'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
