import random
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import Dispositivo, Funcionario, Paciente, Leitura, Classificacao

NOMES = [
    'João Silva', 'Marcos Almeida', 'Renato Costa', 'Paulo Henrique',
    'Carlos Eduardo', 'Antônio Ferreira', 'José Ribeiro',
]


class Command(BaseCommand):
    help = 'Cria um paciente, funcionário, dispositivo e leituras de PSA aleatórias para testar o gráfico e o relatório.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cpf', default='11122233344',
            help='CPF (só números) do paciente de teste. Padrão: 11122233344'
        )
        parser.add_argument(
            '--senha', default='teste123',
            help='Senha do paciente de teste. Padrão: teste123'
        )
        parser.add_argument(
            '--leituras', type=int, default=6,
            help='Quantas leituras gerar. Padrão: 6'
        )

    def handle(self, *args, **options):
        cpf = options['cpf']
        senha = options['senha']
        qtd_leituras = options['leituras']
        nome = random.choice(NOMES)

        dispositivo, _ = Dispositivo.objects.get_or_create(
            identificador='A102',
            defaults={'localidade': 'Unidade Centro'}
        )

        func_user, criado = User.objects.get_or_create(
            username='99988877766',
            defaults={'first_name': 'Ana Pereira'}
        )
        if criado:
            func_user.set_password('teste123')
            func_user.save()
        funcionario, _ = Funcionario.objects.get_or_create(
            usuario=func_user,
            defaults={
                'nome_completo': 'Ana Pereira',
                'cpf': '99988877766',
                'cargo': 'Técnica de enfermagem',
                'localidade': 'Unidade Centro',
            }
        )

        user, criado = User.objects.get_or_create(
            username=cpf,
            defaults={'first_name': nome}
        )
        user.set_password(senha)
        user.first_name = nome
        user.save()

        paciente, _ = Paciente.objects.update_or_create(
            usuario=user,
            defaults={
                'nome_completo': nome,
                'cpf': cpf,
                'email': 'paciente.teste@exemplo.com',
                'telefone': '(11) 90000-0000',
                'endereco': 'Rua Exemplo, 123',
                'data_nascimento': timezone.now().date().replace(year=timezone.now().year - 58),
                'dispositivo': dispositivo,
            }
        )

        Leitura.objects.filter(paciente=paciente).delete()

        hoje = timezone.now()
        for i in range(qtd_leituras):
            valor = round(random.uniform(1.5, 3.8), 2)
            risco_forcado = None
            if i == qtd_leituras - 2:
                valor = round(random.uniform(4.2, 6.5), 2)  # uma leitura fora da referência
                risco_forcado = 'alto'

            leitura = Leitura.objects.create(
                paciente=paciente,
                dispositivo=dispositivo,
                funcionario=funcionario,
                medicao=valor,
            )
            data_simulada = hoje - timedelta(days=30 * (qtd_leituras - i))
            Leitura.objects.filter(pk=leitura.pk).update(data_hora=data_simulada)

            nivel_risco = risco_forcado or random.choices(
                ['baixo', 'moderado', 'alto'], weights=[6, 3, 1]
            )[0]
            if nivel_risco == 'alto':
                cor_r, cor_g, cor_b = random.randint(200, 235), random.randint(40, 80), random.randint(30, 70)
            elif nivel_risco == 'moderado':
                cor_r, cor_g, cor_b = random.randint(220, 245), random.randint(170, 200), random.randint(30, 70)
            else:
                cor_r, cor_g, cor_b = random.randint(60, 110), random.randint(160, 200), random.randint(80, 120)

            Classificacao.objects.create(
                leitura=leitura,
                cor_r=cor_r, cor_g=cor_g, cor_b=cor_b,
                nivel_risco=nivel_risco,
            )

        self.stdout.write(self.style.SUCCESS(
            f'\nPaciente de teste criado: {nome}\n'
            f'CPF (login): {cpf}\n'
            f'Senha: {senha}\n'
            f'{qtd_leituras} leituras geradas (uma delas acima da referência e com risco alto).\n'
            f'Cada leitura já tem uma cor/classificação de risco de exemplo.\n'
            f'Entre em http://127.0.0.1:8000/ com esse CPF e senha para ver o relatório.\n'
        ))
