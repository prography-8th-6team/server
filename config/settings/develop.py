from config.settings import *

DEBUG = True

SECRET_KEY = env('DEV_SECRET_KEY')

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME'),
        'HOST': env('DATABASE_HOST'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'PORT': env('DATABASE_PORT'),
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

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_REGION = 'ap-northeast-2'

AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
