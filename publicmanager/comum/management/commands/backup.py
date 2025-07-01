import os
import subprocess
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Realiza o backup do banco de dados e armazena no diretório de backup'

    def handle(self, *args, **kwargs):
        try:
            db_host = settings.POSTGRES_HOST
            db_port = settings.POSTGRES_PORT
            db_user = settings.POSTGRES_USER
            db_password = settings.POSTGRES_PASSWORD
            db_name = settings.POSTGRES_DB

            if not all([db_host, db_port, db_user, db_password, db_name]):
                raise ValueError("Todas as variáveis de ambiente do banco de dados devem estar definidas")
            
            project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

            backup_dir = os.path.join(project_dir, 'backup')
            os.makedirs(backup_dir, exist_ok=True)

            file = f"backup_{db_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"

            backup_file = os.path.join(backup_dir, file)

            # Executar o comando pg_dump
            pg_dump_command = [
                'pg_dump',
                '-h', db_host,
                '-p', db_port,
                '-U', db_user,
                '-F', 'c',
                '-b',
                '-f', backup_file,
                db_name
            ]

            env = os.environ.copy()
            env['PGPASSWORD'] = db_password

            subprocess.run(pg_dump_command, env=env, check=True)

            self.stdout.write(self.style.SUCCESS(f"Backup criado com sucesso em {file}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro ao executar o backup: {e}"))
