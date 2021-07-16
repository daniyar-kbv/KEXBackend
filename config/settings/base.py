import base64
import os
from collections import OrderedDict
from datetime import timedelta

from . import Languages
from config.constants.error_messages import ERROR_MESSAGES
from config.constants.contacts import CONTACTS

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

SECRET_KEY = '8e@ww05^%&0n^9x1vi#&3_a0%nfvd72#=yn@=hbkc6fdsw$t0c'

# OTP settings
HOTP_KEY = base64.b32encode(SECRET_KEY.encode("utf-8"))
OTP_LENGTH = 4
OTP_VALIDITY_PERIOD = 5  # in minutes

DEBUG = True

ALLOWED_HOSTS = ["*"]

CONSTANCE_CONFIG = {
    "IIKO_SERVICE_HOST": ("https://api-ru.iiko.services", "IIKO service host"),
    "IIKO_AUTH_TOKEN_LIFETIME": (60 * 30, "IIKO auth token lifetime in seconds"),
    **ERROR_MESSAGES,
    **CONTACTS,
}

CONSTANCE_CONFIG_FIELDSETS = OrderedDict([
    ("Contacts", tuple(CONTACTS.keys())),
    ("IIKO Credentials&settings", (
        "IIKO_SERVICE_HOST",
        "IIKO_AUTH_TOKEN_LIFETIME",
    )),
    ("Error messages", tuple(ERROR_MESSAGES.keys())),
])

CONSTANCE_REDIS_CONNECTION = {
    'host': os.getenv("REDIS_HOST", "localhost"),
    'port': 6379,
    'db': 0,
}
THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",
    # "django_filters",
    "corsheaders",
    "phonenumber_field",
    "constance",
    "django_celery_beat",
    "ckeditor",
    "ckeditor_uploader",
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


LOCAL_APPS = [
    'apps.sms.apps.SmsConfig',
    'apps.users.apps.UsersConfig',
    'apps.common.apps.CommonConfig',
    'apps.orders.apps.OrdersConfig',
    'apps.partners.apps.PartnersConfig',
    'apps.location.apps.LocationConfig',
    'apps.pipeline.apps.PipelineConfig',
    'apps.nomenclature.apps.NomenclatureConfig',
    'apps.translations.apps.TranslationsConfig',
    'apps.promotions.apps.PromotionsConfig',
    'apps.docs.apps.DocsConfig',
    'apps.notifications.apps.NotificationsConfig'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

AUTH_USER_MODEL = "users.User"


MIDDLEWARE = [
    'apps.translations.middleware.LanguageHeaderMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'apps.common.middleware.HandleAPIResponsesMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'config.server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "kexdb"),
        "USER": os.getenv("DB_USER", "kexdb"),
        "PASSWORD": os.getenv("DB_PASSWORD", "kexdb"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


CORS_ALLOW_ALL_ORIGINS = True

# LOGGING = {
#     'version': 1,
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         }
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#         }
#     },
#     'loggers': {
#         'django.db.backends': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#         }
#     }
# }
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
DEFAULT_LANGUAGE = Languages.RUSSIAN
LANGUAGE_CODE = "ru"
TIME_ZONE = "Asia/Almaty"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = os.getenv("STATIC_URL", "/static/")
STATIC_ROOT = os.getenv("STATIC_ROOT", os.path.join(BASE_DIR, 'static'))
# STATIC_DIR = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [STATIC_DIR]

INSTAGRAM_CLIENT_ID = "478461956554478"
INSTAGRAM_CLIENT_SECRET = "4824cd7ac54b0b07c8e6653d8478fcc2"
INSTAGRAM_REDIRECT_URI = "/auth/instagram/"

MEDIA_URL = os.getenv("MEDIA_URL", "/media/")
MEDIA_ROOT = os.getenv("MEDIA_ROOT", os.path.join(BASE_DIR, "media"))

# FIREBASE CLOUD MESSAGING (FCM)
GOOGLE_APPLICATION_CREDENTIALS = os.path.join(BASE_DIR, "google-credentials.json") # service account in Firebase Project


CKEDITOR_UPLOAD_PATH = "ncrm_helper"
# CKEDITOR_CONFIGS = {
#     'default': {
#         'toolbar': 'full',
#         'height': 600,
#         'width': 1200,
#     },
# }
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',
                'Youtube'
            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        # 'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath',
            'youtube'
        ]),
    }
}


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    'COERCE_DECIMAL_TO_STRING': False,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("JWT",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "api_key": {"type": "apiKey", "name": "Authorization", "in": "header"},
    },
    "DEEP_LINKING": True,
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{os.getenv('REDIS_HOST', 'localhost')}:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


# Celery settings
CELERY_BROKER_URL = "{protocol}://{user}:{pwd}@{host}:{port}/{vhost}".format(
    protocol=os.getenv("RABBIT_PROTOCOL", "pyamqp"),
    user=os.getenv("RABBIT_USER", "guest"),
    pwd=os.getenv("RABBIT_PASSWORD", "guest"),
    host=os.getenv("RABBIT_HOST", "localhost"),
    port=os.getenv("RABBIT_PORT", "5672"),
    vhost=os.getenv("RABBIT_VHOST", "/"),
)
CELERY_RESULT_BACKEND = "redis://{host}:{port}/{db_index}".format(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=os.getenv("REDIS_PORT", "6379"),
    db_index=os.getenv("CELERY_REDIS_DB_INDEX", "0"),
)
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"

CELERY_RESULT_EXTENDED = False
CELERY_RESULT_EXPIRES = 3600
CELERY_ALWAYS_EAGER = False
CELERY_ACKS_LATE = True
CELERY_TASK_PUBLISH_RETRY = True
CELERY_DISABLE_RATE_LIMITS = False
CELERY_TASK_TRACK_STARTED = True

# LOGGING = {
#     'version': 1,
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         }
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#         }
#     },
#     'loggers': {
#         'django.db.backends': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#         }
#     }
# }
