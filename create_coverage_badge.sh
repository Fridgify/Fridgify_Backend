#!/../bin/sh
echo "create code coverage badge"
ls
rm -r coverage # Python image doesnt seem to have the necessary cli tools 
mkdir coverage
python manage.py makemigrations Fridgify_Backend --settings=Fridgify_Backend.settings.local
python manage.py migrate Fridgify_Backend --settings=Fridgify_Backend.settings.local
python manage.py test --settings=Fridgify_Backend.settings.local
mv .coverage ./coverage
cd coverage
coverage-badge -o coverage.svg
