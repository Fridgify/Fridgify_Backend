#!/../bin/sh
echo "testing"

if python manage.py test --settings=Fridgify_Backend.settings.testing; then
    echo "Command succeeded"
    exit 0
else
    echo "Command failed"
    exit 1
fi

