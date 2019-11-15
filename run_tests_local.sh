#!/../bin/sh
echo "testing"

python manage.py makemigrations Fridgify_Backend --settings=Fridgify_Backend.settings.local
python manage.py migrate Fridgify_Backend --settings=Fridgify_Backend.settings.local
if python manage.py test --settings=Fridgify_Backend.settings.local; then
    echo "Command succeeded"
    exit 0
else
    echo "Command failed"
    exit 1
fi

