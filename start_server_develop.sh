#!/bin/bash
python manage.py makemigrations Fridgify_Backend --settings=Fridgify_Backend.settings.develop
echo "Made Migrations"
python manage.py migrate Fridgify_Backend --settings=Fridgify_Backend.settings.develop
echo "Migrate changes"
python manage.py runserver 0.0.0.0:9999 --settings=Fridgify_Backend.settings.develop
echo "Started server"
