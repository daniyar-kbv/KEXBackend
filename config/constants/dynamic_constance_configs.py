import os

from .error_messages import ERROR_MESSAGES

CONSTANCE_REDIS_CONNECTION = {
    'host': 'redis',
    'port': 6379,
    'db': 0,
}

CONSTANCE_CONFIG = {
    "IIKO_SERVICE_HOST": ("https://api-ru.iiko.services", "IIKO service host"),
    "IIKO_AUTH_TOKEN_LIFETIME": (60 * 30, "IIKO auth token lifetime in seconds"),
    **ERROR_MESSAGES,
}

CONSTANCE_CONFIG_FIELDSETS = {
    "IIKO Credentials&settings": (
        "IIKO_SERVICE_HOST",
        "IIKO_AUTH_TOKEN_LIFETIME",
    ),
    "Error messages": (
        tuple(ERROR_MESSAGES.keys())
    ),
}
