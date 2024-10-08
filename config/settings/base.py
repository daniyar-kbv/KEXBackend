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
ENCRYPTION_KEY = 'bkc6e@ww0fds7%&32&0n^9x1vi#85^=yn*2hw_a0%nfvd#$t0c'

# OTP settings
HOTP_KEY = base64.b32encode(SECRET_KEY.encode("utf-8"))
OTP_LENGTH = 4
OTP_VALIDITY_PERIOD = 1.5  # in minutes

DEBUG = True

ALLOWED_HOSTS = ["*"]

CONSTANCE_CONFIG = {
    "IIKO_SERVICE_HOST": ("https://api-ru.iiko.services", "IIKO service host"),
    "IIKO_AUTH_TOKEN_LIFETIME": (60 * 30, "IIKO auth token lifetime in seconds"),
    "CLOUDPAYMENTS_HOST": ("https://api.cloudpayments.ru", ""),
    "CLOUDPAYMENTS_PUBLIC_KEY": ("pk_2ec019c3a3a24b44996a1a2ca6f8c", ""),
    "CLOUDPAYMENTS_SECRET_KEY": ("3da278f77c31ca71b652a25a85b65826", ""),
    "IOS_ON": (True, "ios devices"),
    "ANDROID_ON": (True, "android devices"),
    "MOBIZON_API_KEY": ('qwerty', ''),
    "SEND_OTP": (False, ''),
    "USE_DEFAULT_OTP": (False, ''),
    "SMS_FREE_PHONES": ('', ''),
    **ERROR_MESSAGES,
    **CONTACTS,
}

CONSTANCE_CONFIG_FIELDSETS = OrderedDict([
    ("Contacts", tuple(CONTACTS.keys())),
    ("SMS", (
        "MOBIZON_API_KEY",
        "SEND_OTP",
        "USE_DEFAULT_OTP",
        "SMS_FREE_PHONES",
    )),
    ("IIKO Credentials&settings", (
        "IIKO_SERVICE_HOST",
        "IIKO_AUTH_TOKEN_LIFETIME",
    )),
    ("CloudPayments credentials", (
        "CLOUDPAYMENTS_HOST",
        "CLOUDPAYMENTS_PUBLIC_KEY",
        "CLOUDPAYMENTS_SECRET_KEY",
    )),
    ("Control devices", (
        "IOS_ON",
        "ANDROID_ON",
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
    'apps.payments.apps.PaymentsConfig',
    'apps.notifications.apps.NotificationsConfig',
    'apps.order_rates.apps.OrderRatesConfig',
    'apps.coupons.apps.CouponsConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

AUTH_USER_MODEL = "users.User"


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'apps.translations.middleware.LanguageHeaderMiddleware',
    'apps.common.middleware.UserAgentMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

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
CORS_ALLOW_CREDENTIALS = True


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
# STATIC_DIR = os.getenv("STATIC_ROOT", os.path.join(BASE_DIR, 'static'))
# STATICFILES_DIRS = [STATIC_DIR]

INSTAGRAM_CLIENT_ID = "478461956554478"
INSTAGRAM_CLIENT_SECRET = "4824cd7ac54b0b07c8e6653d8478fcc2"
INSTAGRAM_VERIFICATION_URI = "https://api.instagram.com/oauth/authorize"
INSTAGRAM_REDIRECT_URI = "/promotions/instagram/"
INSTAGRAM_PARAMETER = "code"

MEDIA_URL = os.getenv("MEDIA_URL", "/media/")
MEDIA_ROOT = os.getenv("MEDIA_ROOT", os.path.join(BASE_DIR, "media"))

# FIREBASE CLOUD MESSAGING (FCM)
GOOGLE_APPLICATION_CREDENTIALS = os.path.join(BASE_DIR, "google-credentials.json")

CKEDITOR_UPLOAD_PATH = "ncrm_helper"
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
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
                'Preview',
                'Maximize',
            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath',
        ]),
    }
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "apps.users.authentication.JWTAuthentication"
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/minute',
        'user': '100/minute'
    }
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