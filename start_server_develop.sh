#!/bin/bash
export DJANGO_SETTINGS_MODULE=fridgify_backend.settings.develop
python manage.py collectstatic --noinput
echo "Collect static files"
python manage.py makemigrations fridgify_backend
echo "Made Migrations"
python manage.py migrate fridgify_backend
echo "Migrate changes"
python manage.py loaddata providers.json
echo "Add fixtures"
python manage.py fill_db
echo "Fill database"
python manage.py runserver 0.0.0.0:9999 --verbosity 3
echo "Started server"
