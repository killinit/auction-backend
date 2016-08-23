"""
Django settings for django_channels.

For more information on settings within this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""


import os
import datetime
from django.utils.translation import ugettext_lazy as _
from kombu import Exchange, Queue


# Set the base directory from which subdirectories will be determined
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


# Security
SECRET_KEY = os.environ['DJ_SECRET_KEY']
#INTERNAL_IPS = ("127.0.0.1", "0.0.0.0", "192.168.99.100", "192.168.99.110")
ALLOWED_HOSTS = [os.environ['DJ_ALLOWED_HOST']]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Debugging
DEBUG = True if os.environ['DJ_DEBUG'] == 'True' else False
if DEBUG == True:
    def show_toolbar(request):
        return True
    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": show_toolbar}


# Application definitions
INSTALLED_APPS = (
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third party
    'channels',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'debug_toolbar',
    'django_extensions',
    'rest_framework_swagger',
    'corsheaders',
    # apps
    'apps.user.apps.UserConfig',
    'apps.auction.apps.AuctionConfig',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    #'audit_log.middleware.JWTAuthMiddleware',
    'audit_log.middleware.UserLoggingMiddleware',
)

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, '../templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(os.environ['REDIS_URL'], int(os.environ['REDIS_PORT']))],
        },
        "ROUTING": "config.routing.channel_routing",
    },
}


# Authentication
AUTH_USER_MODEL = 'user.User'

REST_FRAMEWORK = {
    #'PAGE_SIZE': 10,
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated', ),
    'DEFAULT_AUTHENTICATION_CLASSES': ( 'rest_framework_jwt.authentication.JSONWebTokenAuthentication', ),
}

DJOSER = {
    #'DOMAIN': 'p2pfeedback.com',
    #'SITE_NAME': 'P2PFeedbackBackend',
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': False,
    'PASSWORD_VALIDATORS': [],
    'SERIALIZERS': {},
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_DECODE_HANDLER': 'rest_framework_jwt.utils.jwt_decode_handler',
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'api.utils.utils.jwt_response_payload_handler',
    'JWT_PAYLOAD_GET_USER_ID_HANDLER': 'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


CORS_ORIGIN_ALLOW_ALL = True
#CORS_URLS_REGEX = r'^/api/.*$'
# CORS_ORIGIN_WHITELIST = (
#         'http://127.0.0.1/',
#         'localhost'
#     )


# Celery (RabbitMQ)
BROKER_URL = 'amqp://{user}:{password}@{host}:{port}/{vhost}'.format(user=os.environ['BROKER_USER'],
                                                                     password=os.environ['BROKER_PASSWORD'],
                                                                     host=os.environ['BROKER_HOST'],
                                                                     port=int(os.environ['BROKER_PORT']),
                                                                     vhost=os.environ['BROKER_VHOST'])
BROKER_POOL_LIMIT = int(os.environ['BROKER_POOL_LIMIT'])
BROKER_CONNECTION_TIMEOUT = int(os.environ['BROKER_CONNECTION_TIMEOUT'])
# We don't want to have dead connections stored on rabbitmq, so we have to negotiate using heartbeats
BROKER_HEARTBEAT = '?heartbeat=30'
if not BROKER_URL.endswith(BROKER_HEARTBEAT):
    BROKER_URL += BROKER_HEARTBEAT

CELERY_DEFAULT_QUEUE = os.environ['BROKER_VHOST']
CELERY_QUEUES = (Queue(os.environ['BROKER_VHOST'],
                       Exchange(os.environ['BROKER_VHOST']),
                       routing_key=os.environ['BROKER_VHOST']),)

# Celery (Redis)
CELERY_IGNORE_RESULT = False
CELERY_RESULT_BACKEND = 'redis://{}:{}/{}'.format(os.environ['REDIS_URL'],
                                                  int(os.environ['REDIS_PORT']),
                                                  int(os.environ['REDIS_DB']))
CELERY_REDIS_MAX_CONNECTIONS = int(os.environ['CELERY_REDIS_MAX_CONNECTIONS'])

# Celery (Other)
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_SEND_TASK_ERROR_EMAILS = False
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 5
CELERY_ENABLE_UTC = True if os.environ['CELERY_ENABLE_UTC'] == 'True' else False
CELERY_TIMEZONE = os.environ['CELERY_TIMEZONE']
CELERY_TASK_PUBLISH_RETRY = True


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_SERVICE'],
        'PORT': os.environ['DB_PORT']
    }
}


# Emails
DJ_EMAIL_USE_CONSOLE = os.environ["DJ_EMAIL_USE_CONSOLE"]
if DJ_EMAIL_USE_CONSOLE == 'True':
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
elif DJ_EMAIL_USE_CONSOLE == 'False':
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = (
    ('pt', _('Portuguese')),
    ('en', _('English')),
)
LOCALE_PATHS = [os.path.join(BASE_DIR, '../locale')]


# Static files
if os.environ['DJ_DEFAULT_FILE_STORAGE']: DEFAULT_FILE_STORAGE = os.environ['DJ_DEFAULT_FILE_STORAGE']
if os.environ['DJ_STATICFILES_STORAGE']: STATICFILES_STORAGE = os.environ['DJ_STATICFILES_STORAGE']
STATIC_URL = os.environ['DJ_STATIC_URL']
MEDIA_URL = os.environ['DJ_MEDIA_URL']
STATIC_ROOT = '/www/static'
MEDIA_ROOT = '/www/media'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static/')),


# Amazon Web Services
if os.environ['AWS_ACCESS_KEY_ID']: AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
if os.environ['AWS_SECRET_ACCESS_KEY']: AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
if os.environ['AWS_STORAGE_BUCKET_NAME']: AWS_ACCESS_KEY_ID = os.environ['AWS_STORAGE_BUCKET_NAME']


# Caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': [
            '{}:{}'.format(os.environ['MEMCACHED_URL'], os.environ['MEMCACHED_PORT']),
        ]
    }
}

# API Docs
SWAGGER_SETTINGS = {
    'api_version': '0.1',
    'is_authenticated': False,
    'is_superuser': False,
    'permission_denied_handler': 'django.contrib.auth.views.login',
    'unauthenticated_user': 'django.contrib.auth.models.AnonymousUser',
    'info': {
        'contact': 'support@druuid.com',
        'description': 'This is a dev server for P2PFeedback project. ',
        'title': 'P2PFeedback',
    },
}

# Instruct Jupyter Notebook to open notebook in remote server
NOTEBOOK_ARGUMENTS = ['--ip=0.0.0.0']

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console':{
            'class':'logging.StreamHandler',
        },
    },
    'root': {
        'level': os.getenv('DJ_LOG_LEVEL', 'INFO'),
        'handlers': ['console']
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': os.getenv('DJ_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'channels': {
            'handlers': ['console'],
            'level': os.getenv('DJ_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'celery': {
            'handlers': ['console'],
            'level': os.getenv('DJ_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'flower': {
            'handlers': ['console'],
            'level': os.getenv('DJ_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'apps': {
            'handlers': ['console'],
            'level': os.getenv('DJ_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'api': {
            'handlers': ['console'],
            'level': os.getenv('DJ_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'utils': {
            'handlers': ['console'],
            'level': os.getenv('DJ_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
    },
}

