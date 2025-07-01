import csv
from django.core.management.base import BaseCommand
from publicmanager.saude_cadastro.models import TipoExame

class Command(BaseCommand):
    help = 'Importação dos tipos de exames.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Gerando dados dos tipos de exames...'))
        
        with open('publicmanager/comum/fixtures/tipos_exames.csv', newline='') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',')
            
            for row in spamreader:
                TipoExame.objects.get_or_create(
                    nome=row['nome'],
                    tipo=row['tipo'],
                )

        self.stdout.write(self.style.SUCCESS('Importação dos tipos de exames gerados com sucesso!'))
