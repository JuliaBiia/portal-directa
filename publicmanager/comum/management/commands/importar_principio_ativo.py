import csv
from django.core.management.base import BaseCommand
from publicmanager.saude_farmacia.models import PrincipioAtivo

class Command(BaseCommand):
    help = 'Importação dos principios ativos.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Gerando dados dos principios ativos...'))
        
        with open('publicmanager/comum/fixtures/tb_principio_ativo.csv', newline='') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',')
            
            for row in spamreader:
                PrincipioAtivo.objects.get_or_create(
                    nome=row['nomeprincipioativo'],
                )

        self.stdout.write(self.style.SUCCESS('Importação dos principio ativos gerados com sucesso!'))
