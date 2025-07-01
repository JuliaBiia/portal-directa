import csv
import random
from django.core.management.base import BaseCommand
from publicmanager.saude.models import UnidadeSaude
from publicmanager.saude_farmacia.models import Medicamento, PrincipioAtivo

class Command(BaseCommand):
    help = 'Importação dos Medicamentos.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Gerando dados dos medicamentos...'))
        
        principios_ativos = PrincipioAtivo.objects.all()
        unidades = UnidadeSaude.objects.all()
        
        with open('publicmanager/comum/fixtures/tb_medicamento_catmat.csv', newline='') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',')
            
            for row in spamreader:
                try:
                    Medicamento.objects.get_or_create(
                        nome_medicamento=row['medicamento_nome'],
                        codigo_de_barra=row['codigo_de_barra'],
                        principio_ativo_medicamento=random.choice(principios_ativos),
                        estoque_minimo_geral=20,
                        unidade_saude=random.choice(unidades),
                    )
                except:
                    pass

        self.stdout.write(self.style.SUCCESS('Importação dos medicamentos gerados com sucesso!'))
