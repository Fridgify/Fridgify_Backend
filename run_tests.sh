#!/../bin/sh
echo "testing"

if python manage.py test ; then
    echo "Command succeeded"
    exit 0
else
    echo "Command failed"
    exit 1
fi

