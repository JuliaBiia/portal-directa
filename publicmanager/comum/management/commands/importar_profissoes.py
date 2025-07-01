import csv
import random
from publicmanager.saude_cadastro.models import Profissao
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Importação das profissões'

    def handle(self, *args, **options):
        with open('publicmanager/comum/fixtures/profissao.csv', newline='') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',')
            
            for profissao in spamreader:
                try:
                    Profissao.objects.create(
                        codigo=random.randint(10000, 99999),
                        titulo=profissao['PROFISSOES']
                    )
                except Exception as e:
                    print(e)

            print("Profissões geradas")
                    
