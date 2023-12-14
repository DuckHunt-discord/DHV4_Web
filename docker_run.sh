git pull --recurse-submodules

python manage.py collectstatic --clear --no-input
python manage.py migrate --no-input --skip-checks

exec gunicorn DHV4_Web.wsgi:application --access-logfile None --error-logfile '-' --log-level "info" --capture-output --bind 0.0.0.0:8080 --workers=4
