#!/usr/bin/env bash
# Script rodado pelo Render antes de ligar o site.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Cria (ou atualiza a senha) do admin, usando as variáveis de ambiente
# DJANGO_SUPERUSER_USERNAME / DJANGO_SUPERUSER_EMAIL / DJANGO_SUPERUSER_PASSWORD
# (definidas no painel do Render). Funciona mesmo sem acesso a Shell, e não
# quebra o build se o usuário já existir.
python manage.py bootstrap_admin

# Gera um paciente de teste com leituras aleatórias, só se a variável de
# ambiente CRIAR_DADOS_TESTE estiver definida como "true" no painel do Render.
if [ "$CRIAR_DADOS_TESTE" = "true" ]; then
  python manage.py criar_dados_teste
fi
