import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        'Cria o superusuário se ele não existir, ou atualiza a senha se já existir. '
        'Usa as variáveis de ambiente DJANGO_SUPERUSER_USERNAME, '
        'DJANGO_SUPERUSER_EMAIL e DJANGO_SUPERUSER_PASSWORD. '
        'Seguro para rodar em todo deploy (não dá erro se já existir).'
    )

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')

        if not username or not password:
            self.stdout.write(self.style.WARNING(
                'DJANGO_SUPERUSER_USERNAME ou DJANGO_SUPERUSER_PASSWORD não '
                'estão definidos nas variáveis de ambiente — nada foi feito.'
            ))
            return

        User = get_user_model()
        usuario, criado = User.objects.get_or_create(
            username=username,
            defaults={'email': email},
        )
        usuario.email = email
        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.set_password(password)
        usuario.save()

        if criado:
            self.stdout.write(self.style.SUCCESS(f'Superusuário "{username}" criado.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superusuário "{username}" já existia — senha atualizada.'))
