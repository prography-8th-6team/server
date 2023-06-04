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

LOGGING['handlers'] = {
    'file': {
        'level': 'INFO',
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': '/home/ubuntu/deploy/server/jerny.log',
        'maxBytes': 10*1024*1024,  # 10MB
        'backupCount': 5,
        'formatter': 'verbose'
    }
}

DEVELOP_LOG_DIR = '/var/log/server/develop/'

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
