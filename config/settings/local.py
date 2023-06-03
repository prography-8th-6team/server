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

DEVELOP_LOG_DIR = '/log/'

LOGGING['handlers'] = {
    'file': {
        'level': 'INFO',
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': f'{DEVELOP_LOG_DIR}jerny.log',
        'maxBytes': 10*1024*1024,  # 10MB
        'backupCount': 5,
        'formatter': 'verbose'
    },
    'error': {
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': f'{DEVELOP_LOG_DIR}/error.log',
        'maxBytes': 10 * 1024 * 1024,  # 10MB
        'backupCount': 5,
        'formatter': 'verbose'
    }
}