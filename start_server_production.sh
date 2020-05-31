#!/bin/bash
export DJANGO_SETTINGS_MODULE=fridgify_backend.settings.production
python manage.py collectstatic --no-input
echo "Collect static files"
python manage.py makemigrations fridgify_backend
echo "Made Migrations"
python manage.py migrate fridgify_backend
echo "Migrate changes"
python manage.py loaddata providers.json
echo "Add fixtures"
python manage.py runserver 0.0.0.0:9000 --verbosity 3
echo "Started server"
