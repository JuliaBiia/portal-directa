from django.core import management
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Configurações de Desenvolvimento'

    def handle(self, *args, **kwargs):

        try:
            #Gerar cids.
            management.call_command('importar_cids')
            print("Cids gerados")

            #Gerar principios ativos.
            management.call_command('importar_principio_ativo')
            print("Principios ativos gerados")

            #Gerar tipos exames.
            management.call_command('importar_tipos_exames')
            print("Tipos exames gerados")

            #Gerar procedimentos.
            management.call_command('importar_procedimentos')
            print("Procedimentos gerados")
            
            #Gerar exames fake.
            management.call_command('gerar_exames_fake')
            print("Exames gerados")

            #Gerar pacientes fake.
            management.call_command('gerar_pacientes_fake')
            print("Pacientes gerados")

            #Gerar profissional.
            management.call_command('gerar_profissionais_fake')
            print("Profissionais gerados")

            #Vincular fotos.
            management.call_command('vincular_fotos_fake')
            print("Vincular foto aos pacientes")

            #Importar medicamentos.
            management.call_command('importar_medicamentos')
            print("Medicamentos gerados")

            #Gerar Setores e Salas fake.
            management.call_command('gerar_setores_salas_fake')
            print("Setores e Salas gerados")

        except Exception as e:
            print(e)