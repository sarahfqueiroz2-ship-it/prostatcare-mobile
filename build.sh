#!/usr/bin/env bash
# Script rodado pelo Render antes de ligar o site.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Cria o admin automaticamente usando as variáveis de ambiente
# DJANGO_SUPERUSER_USERNAME / DJANGO_SUPERUSER_EMAIL / DJANGO_SUPERUSER_PASSWORD
# (definidas no painel do Render). Se o usuário já existir, ignora o erro
# e continua o deploy normalmente — não precisa de acesso a Shell.
python manage.py createsuperuser --noinput || true
python manage.py criar_admin
