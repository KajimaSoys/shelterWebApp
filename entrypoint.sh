#!/bin/bash

python manage.py migrate
python manage.py init_db
python manage.py collectstatic --noinput
exec gunicorn shelterWebApp.wsgi:application --bind 0.0.0.0:8000


