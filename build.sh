#!/usr/bin/env bash
# Script rodado pelo Render antes de ligar o site.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
