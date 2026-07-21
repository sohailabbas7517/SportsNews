#!/usr/bin/env bash

set -o errexit

echo "==> Installing dependencies..."
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --noinput

echo "==> Applying database migrations..."
python manage.py migrate

echo "==> Creating/updating admin user..."
python manage.py create_admin

echo "==> Build completed successfully."