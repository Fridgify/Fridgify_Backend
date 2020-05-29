#!/../bin/sh
echo "Run locally..."

set -a && [ -f ./.env ] && . ./.env && set +a

python manage.py makemigrations fridgify_backend --settings=fridgify_backend.settings.local
python manage.py migrate fridgify_backend --settings=fridgify_backend.settings.local
python manage.py loaddata providers.json
python manage.py fill_db
python manage.py runserver --settings=fridgify_backend.settings.local
