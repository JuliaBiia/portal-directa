import csv
from django.core.management.base import BaseCommand
from publicmanager.saude_cadastro.models import CID

class Command(BaseCommand):
    help = 'Importação dos cids.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Gerando dados dos cids...'))
        
        with open('publicmanager/comum/fixtures/cids.csv', newline='') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',')
            
            for row in spamreader:
                CID.objects.get_or_create(
                    codigo=row['codigo'],
                    defaults={'nome': row['nome'],}  
                )

        self.stdout.write(self.style.SUCCESS('Importação dos cids gerados com sucesso!'))
