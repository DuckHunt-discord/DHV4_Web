python manage.py collectstatic --clear --no-input
python manage.py migrate --no-input

exec gunicorn DHV4_Web.wsgi:application --access-logfile '-' --error-logfile '-' --log-level "debug" --capture-output True --bind 0.0.0.0:8080 --workers=4
