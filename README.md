# ProstatCare Mobile — Django + PostgreSQL

Sistema com 3 páginas (login, cadastro, gráfico+relatório) e 3 perfis de
acesso (admin, funcionário, paciente), backend em Django e banco PostgreSQL.

## Estrutura

```
prostatcare_django/
├── manage.py
├── requirements.txt
├── .env.example           # copie para .env e ajuste
├── prostatcare/            # settings, urls, wsgi/asgi
└── core/
    ├── models.py            # Dispositivo, Paciente, Funcionario, Leitura, Relatorio
    ├── forms.py             # PacienteForm, FuncionarioForm, RelatorioForm, LoginForm
    ├── views.py             # login, cadastro, relatorio (com lógica real)
    ├── permissions.py       # controle de acesso por perfil
    ├── urls.py
    ├── admin.py
    ├── templates/core/      # login.html, cadastro.html, relatorio.html, base.html
    └── static/core/         # css e js
```

## Modelo de dados (equivalente ao seu ER)

- **Dispositivo**: identificador, localidade
- **Paciente**: ligado a um usuário (login), dados pessoais, dispositivo padrão
- **Funcionario**: ligado a um usuário (login), cargo, localidade
- **Leitura**: paciente (N:1), dispositivo (N:1), funcionário responsável, valor de PSA (`medicao`), data/hora
- **Relatorio**: 1:1 com uma Leitura — observação, nome de quem assina, data da assinatura

O perfil **admin** é qualquer usuário com `is_staff`/`is_superuser` (o próprio
admin do Django). Paciente e Funcionário têm login próprio, criado junto do
cadastro (usuário = CPF, senha = a que você definir no formulário).

## Como rodar

### 1. Banco de dados

Instale o PostgreSQL, se ainda não tiver:
```bash
sudo apt install postgresql
```

Crie o banco e o usuário (ajuste a senha):
```bash
sudo -u postgres psql
CREATE DATABASE prostatcare;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE prostatcare TO postgres;
\q
```

### 2. Ambiente Python

```bash
cd prostatcare_django
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configuração

```bash
cp .env.example .env
```
Abra o `.env` e ajuste `DB_USER`, `DB_PASSWORD`, `DB_NAME` se necessário.

### 4. Migrações

```bash
python manage.py makemigrations core
python manage.py migrate
```

### 5. Criar o admin

```bash
python manage.py createsuperuser
```
Use um usuário e senha à sua escolha — esse login entra como perfil **admin**.

### 6. Cadastrar um dispositivo

Antes de cadastrar pacientes, crie ao menos um Dispositivo pelo admin do Django:
```bash
python manage.py runserver
```
Acesse http://127.0.0.1:8000/admin/, faça login com o superusuário e
adicione um Dispositivo (identificador + localidade).

### 7. Usar o sistema

- **http://127.0.0.1:8000/** → login (CPF + senha)
- **http://127.0.0.1:8000/cadastro/** → cadastro de paciente (e funcionário, se admin)
- **http://127.0.0.1:8000/relatorio/** → busca paciente, mostra gráfico e permite emitir relatório

O admin loga com o usuário/senha do `createsuperuser`. Funcionário e paciente
logam com o CPF e a senha definidos na tela de cadastro.

## Sobre as leituras

Este projeto não inclui a integração real com o dispositivo (isso depende do
hardware do seu professor). Para testar o gráfico, crie algumas `Leitura`
pelo /admin/ (paciente + dispositivo + valor de PSA) — o gráfico e o
relatório são montados automaticamente a partir delas.
