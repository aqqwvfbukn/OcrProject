python manage.py collectstatic --noinput&&
python manage.py makemigrations&&
python manage.py migrate&&
gunicorn OcrProject.wsgi:application -c gunicorn.conf