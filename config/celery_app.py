import os
from celery import Celery

if not ("DJANGO_SETTINGS_MODULE" in os.environ):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery("kex")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
