from dotenv import load_dotenv

from .base import *  # noqa

load_dotenv()

DEBUG = True

INSTALLED_APPS += ["django_extensions"]  # noqa F405

if DEBUG_TOOLBAR_ENABLED:  # noqa F405
    INSTALLED_APPS += ["debug_toolbar"]  # noqa
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405

PROCESSING_RETURN_URL = "http://localhost:8000/terminal/"

INTERNAL_IPS = ["127.0.0.1"]
CACHES["LOCATION"] = "redis://localhost:6379/1"  # noqa

# LANGUAGES_BIDI = ['ru', 'kz', 'kk']

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"level": "DEBUG", "class": "logging.StreamHandler"}},
    "loggers": {"django.db.backends": {"handlers": ["console"], "level": "INFO"}},
}

CONSTANCE_REDIS_CONNECTION["host"] = "localhost"  # noqa
