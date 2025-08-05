#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

set -o allexport
source ./.env
set +o allexport

python manage.py createsuperuser --no-input