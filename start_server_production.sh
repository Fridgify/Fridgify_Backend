#!/bin/bash
python manage.py makemigrations Fridgify_Backend --settings=Fridgify_Backend.settings.production
echo "Made Migrations"
python manage.py migrate Fridgify_Backend --settings=Fridgify_Backend.settings.production
echo "Migrate changes"
python manage.py runserver 0.0.0.0:9000 --settings=Fridgify_Backend.settings.production
echo "Started server"