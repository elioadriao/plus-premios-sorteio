#!/bin/bash

python manage.py collectstatic --no-input
python manage.py migrate
DJANGO_SUPERUSER_PASSWORD=123456 \
DJANGO_SUPERUSER_WHATSAPP=000000 \
DJANGO_SUPERUSER_NAME=Helio \
./manage.py createsuperuser \
--no-input
gunicorn sortition.wsgi -b 0.0.0.0:8000
