import os
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Restaura o banco de dados a partir de um arquivo SQL'

    def handle(self, *args, **options):
        sql_file = 'dados_completos.sql'
        
        if not os.path.exists(sql_file):
            self.stdout.write(self.style.ERROR(f'Arquivo {sql_file} não encontrado!'))
            return
        
        with open(sql_file, 'r') as f:
            sql = f.read()
        
        with connection.cursor() as cursor:
            try:
                cursor.execute(sql)
                self.stdout.write(self.style.SUCCESS('✅ Banco restaurado com sucesso!'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Erro: {e}'))
