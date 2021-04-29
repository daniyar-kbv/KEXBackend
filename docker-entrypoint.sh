#!/bin/sh
container_type=${CONTAINER_TYPE-DJANGO};
celery_loglevel=${CELERY_LOGLEVEL-INFO};
if [ $container_type = "CELERY" ]; then
  celery -A config.celery_app worker --concurrency 4 --loglevel=$celery_loglevel
elif [ $container_type = "BEAT" ]; then
  celery -A config.celery_app beat --loglevel=info
elif [ $container_type = "FLOWER" ]; then
  celery flower -A config.celery_app --persistent=True
else
  python manage.py migrate --noinput
  uwsgi --ini /app/config/server/uwsgi.ini
fi;
