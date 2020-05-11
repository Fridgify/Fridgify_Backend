#!/../bin/sh
echo "testing"
python manage.py makemigrations Fridgify_Backend --settings=Fridgify_Backend.settings.testing
python manage.py migrate Fridgify_Backend --settings=Fridgify_Backend.settings.testing
if python manage.py test --settings=Fridgify_Backend.settings.testing; then
  echo "Command succeeded"
  exit 0
else
  echo "Command failed"
  exit 1
fi
