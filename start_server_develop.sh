#!/bin/bash
export DJANGO_SETTINGS_MODULE=Fridgify_Backend.settings.develop
python manage.py collectstatic --noinput
echo "Collect static files"
python manage.py makemigrations Fridgify_Backend
echo "Made Migrations"
python manage.py migrate Fridgify_Backend
echo "Migrate changes"
python manage.py loaddata providers.json
echo "Add fixtures"
python manage.py fill_db
echo "Fill database"
python manage.py runserver 0.0.0.0:9999 --verbosity 3
echo "Started server"
