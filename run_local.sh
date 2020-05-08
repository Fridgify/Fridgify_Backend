#!/../bin/sh
echo "Run locally..."

python manage.py makemigrations Fridgify_Backend --settings=Fridgify_Backend.settings.local
python manage.py migrate Fridgify_Backend --settings=Fridgify_Backend.settings.local
# python manage.py loaddata providers.json
python manage.py fill_db
python manage.py runserver --settings=Fridgify_Backend.settings.local
