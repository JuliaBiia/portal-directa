import csv
from django.core.management.base import BaseCommand
from publicmanager.comum.models import Banco

from publicmanager.saude_atendimento.models import Paciente

class Command(BaseCommand):
    help = 'Vincular RG dos Pacientes.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Vinculando RG dos Pacientes ...'))

        with open('publicmanager/comum/fixtures/tb_pacientes.csv', newline='') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',')
            for row in spamreader:
                
                try:
                    paciente = Paciente.objects.get(cpf=row['cpf'])
                    paciente.rg = row['rg']
                    paciente.rg_data = row['rg_data']
                    paciente.save()
                except:
                   pass

        self.stdout.write(self.style.SUCCESS('RG Vinculados com sucesso!'))
