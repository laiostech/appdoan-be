#!/bin/bash
set -e

echo "Waiting for database..."
while ! nc -z $MYSQL_HOST $MYSQL_PORT; do
  sleep 0.1
done
echo "Database is ready!"

echo "Making migrations..."
python manage.py makemigrations --noinput

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating superuser..."
python manage.py shell << 'PYEOF'
from apps.user_management.models import User
import os

username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin123')
email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        full_name='Administrator'
    )
    print(f'Superuser "{username}" created successfully')
else:
    print(f'Superuser "{username}" already exists')
PYEOF

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear || true

echo "Starting server..."
exec "$@"

