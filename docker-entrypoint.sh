#!/bin/sh
container_type=${CONTAINER_TYPE-DJANGO};
celery_loglevel=${CELERY_LOGLEVEL-INFO};

if [ $container_type = "CELERY" ]; then
  celery -A config.celery_app worker --concurrency 4 --loglevel=$celery_loglevel

elif [ $container_type = "GEVENT-CELERY" ]; then
  celery -A config.celery_app worker --loglevel=$celery_loglevel --queues=celery-gevent --pool=gevent --concurrency=200

elif [ $container_type = "BEAT" ]; then
  celery -A config.celery_app beat --loglevel=info

elif [ $container_type = "FLOWER" ]; then
  celery flower -A config.celery_app --persistent=True

else
  python manage.py collectstatic --noinput --clear
  python manage.py migrate --noinput
  uwsgi --ini /app/config/server/uwsgi.ini
fi;
