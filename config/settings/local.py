from dotenv import load_dotenv

from .base import *  # noqa

load_dotenv()

DEBUG = True

INSTALLED_APPS += ["django_extensions"]  # noqa F405

CACHES["LOCATION"] = f"redis://{os.getenv('REDIS_HOST', 'localhost')}:6379/1"  # noqa

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"level": "DEBUG", "class": "logging.StreamHandler"}},
    "loggers": {"django.db.backends": {"handlers": ["console"], "level": "INFO"}},
}

CONSTANCE_REDIS_CONNECTION["host"] = os.getenv("REDIS_HOST", "localhost")  # noqa
