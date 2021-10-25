import os
from celery import Celery
from kombu import Exchange, Queue

if not ("DJANGO_SETTINGS_MODULE" in os.environ):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery("kex")

app.conf.task_queues = [
    Queue("celery", Exchange("celery"), routing_key="celery"),
    Queue("celery-gevent", Exchange('celery-gevent'), routing_key="celery-gevent"),
]

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
