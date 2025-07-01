import os
import random
from faker import Faker
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from publicmanager.saude_atendimento.models import Paciente

class Command(BaseCommand):
    help = 'Vincular fotos fake no perfil do paciente para teste de sistema'

    def handle(self, *args, **options):
        pacientes = Paciente.objects.all()

        pasta_fotos_homens = os.path.join(settings.MEDIA_ROOT, 'imagens/pacientes/homens')
        pasta_fotos_mulheres = os.path.join(settings.MEDIA_ROOT, 'imagens/pacientes/mulheres')

        arquivos_fotos_homens = [f for f in os.listdir(pasta_fotos_homens) if os.path.isfile(os.path.join(pasta_fotos_homens, f))]
        arquivos_fotos_mulheres = [f for f in os.listdir(pasta_fotos_mulheres) if os.path.isfile(os.path.join(pasta_fotos_mulheres, f))]

        for paciente in pacientes:
            
            if paciente.sexo == 'M':
                foto_selecionada = random.choice(arquivos_fotos_homens)
                caminho_relativo_foto = os.path.join('/imagens/pacientes/homens/', foto_selecionada)
            else:
                foto_selecionada = random.choice(arquivos_fotos_mulheres)
                caminho_relativo_foto = os.path.join('/imagens/pacientes/mulheres/', foto_selecionada)

            paciente.foto_paciente = caminho_relativo_foto
            paciente.save()

        self.stdout.write(self.style.SUCCESS('Fotos vinculadas com sucesso!'))