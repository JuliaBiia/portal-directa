import csv
from django.core.management.base import BaseCommand
from publicmanager.saude_cadastro.models import Procedimento

class Command(BaseCommand):
    help = 'Importação dos procedimentos.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Gerando dados dos procedimentos...'))
        
        with open('publicmanager/comum/fixtures/procedimentos.csv', newline='') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',')
            
            for row in spamreader:
                procedimento, created = Procedimento.objects.get_or_create(
                    codigo=row['codigo'],
                    defaults={'nome': row['nomeprocedimento'],}  
                )
                procedimento.nome = row['nomeprocedimento']
                procedimento.save()

        self.stdout.write(self.style.SUCCESS('Importação dos procedimentos gerados com sucesso!'))
