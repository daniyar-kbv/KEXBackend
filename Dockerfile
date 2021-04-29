FROM python:3.7

RUN apt-get update && apt-get install -y gettext libgettextpo-dev

COPY ./requirements/base.txt ./requirements/production.txt /
RUN pip install --upgrade pip && pip install -r /production.txt

# Set volume for database and static files.
RUN mkdir -p /static /media /flower_db

# Set docker-entrypoint
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Set env variables
ENV DJANGO_SETTINGS_MODULE=config.settings.development
ENV PORT 8000
ENV STATIC_ROOT /static
ENV MEDIA_ROOT /media

WORKDIR /app

# Copy source code
COPY . /app

# Collect static
RUN python manage.py collectstatic --noinput --clear

CMD ["/docker-entrypoint.sh"]
