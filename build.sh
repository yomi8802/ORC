set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
which tesseract
python manage.py superuser