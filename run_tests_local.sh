#!/../bin/sh
echo "testing"

set -a && [ -f ./.env ] && . ./.env && set +a

python manage.py makemigrations fridgify_backend --settings=fridgify_backend.settings.local
python manage.py migrate fridgify_backend --settings=fridgify_backend.settings.local
if python manage.py test --settings=fridgify_backend.settings.local; then
    echo "Command succeeded"
    exit 0
else
    echo "Command failed"
    exit 1
fi

