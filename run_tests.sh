#!/../bin/sh
echo "testing"
python manage.py makemigrations fridgify_backend --settings=fridgify_backend.settings.testing
python manage.py migrate fridgify_backend --settings=fridgify_backend.settings.testing
if python manage.py test --settings=fridgify_backend.settings.testing; then
  echo "Command succeeded"
  exit 0
else
  echo "Command failed"
  exit 1
fi
