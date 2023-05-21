from config.settings import *

DEBUG = False

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'storages',
]

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

WSGI_APPLICATION = 'config.wsgi.deploy.application'

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'DEBUG',
        'handlers': ['file']},
    'formatters': {
        'verbose': {
            'format': (
                '%(asctime)s %(levelname)s %(name)s %(message)s'
                ' [PID:%(process)d:%(threadName)s]')},
        'simple': {
            'format': '%(levelname)s %(message)s'}},
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'}},
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/home/ubuntu/server/test.log',
            'maxBytes': 10*1024*1024,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose'}
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True},
        'django.server': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True},
        'django.db.backends': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True},
        'unicommerce': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True}
    }}