release: python manage.py migrate
web: python manage.py collectstatic --noinput && gunicorn commerce.wsgi --log-file -
