#!/bin/sh

set -e

# Run the application
python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py load_locations


uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi
