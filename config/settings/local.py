from config.settings import *

DEBUG = True

SECRET_KEY = env('LOCAL_SECRET_KEY')

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

WSGI_APPLICATION = 'config.wsgi.local.application'

STATIC_URL = 'static/'

log_path = BASE_DIR

LOGGING['handlers'] = {
    'file': {
        'level': 'INFO',
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': f'{log_path}jerny.log',
        'maxBytes': 10*1024*1024,  # 10MB
        'backupCount': 5,
        'formatter': 'verbose'
    },
    'error': {
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': f'{log_path}/error.log',
        'maxBytes': 10 * 1024 * 1024,  # 10MB
        'backupCount': 5,
        'formatter': 'verbose'
    }
}