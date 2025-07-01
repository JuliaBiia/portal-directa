import random
from faker import Faker
from django.core.management.base import BaseCommand

from publicmanager.saude.models import UnidadeSaude
from publicmanager.saude_farmacia.models import Medicamento, PrincipioAtivo
from publicmanager.saude_cadastro.models import Exame, TipoExame

class Command(BaseCommand):
    help = 'Gerar exames fake no banco de dados'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Gerando exames fake...'))
        fake = Faker(['pt_BR'])

        tipos_exames = TipoExame.objects.all()

        exames_types = [
            ('HEMOGRAMA', 'HEMOGRAMA'),
            ('COLESTEROL_TOTAL', 'COLESTEROL TOTAL'),
            ('GLICEMIA_EM_JEJUM', 'GLICEMIA EM JEJUM'),
            ('TESTE_DE_GRAVIDEZ', 'TESTE DE GRAVIDEZ'),
            ('URINA_TIPO_I', 'URINA TIPO I'),
            ('HEMOCULTURA', 'HEMOCULTURA'),
            ('RADIOGRAFIA_DE_TÓRAX', 'RADIOGRAFIA DE TÓRAX'),
            ('ULTRASSONOGRAFIA_ABDOMINAL', 'ULTRASSONOGRAFIA ABDOMINAL'),
            ('ELETROCARDIOGRAMA', 'ELETROCARDIOGRAMA'),
            ('TOMOGRAFIA_COMPUTADORIZADA', 'TOMOGRAFIA COMPUTADORIZADA'),
            ('RESSONÂNCIA_MAGNÉTICA', 'RESSONÂNCIA MAGNÉTICA'),
            ('EXAME_DE_SANGUE_OCULTO_NAS_FEZES', 'EXAME DE SANGUE OCULTO NAS FEZES'),
            ('DOSAGEM_DE_CREATININA', 'DOSAGEM DE CREATININA'),
            ('TESTE_DE_TOLERÂNCIA_À_GLICOSE', 'TESTE DE TOLERÂNCIA À GLICOSE'),
            ('EXAME_DE_URINA_24_HORAS', 'EXAME DE URINA 24 HORAS')
        ]

        for index, (exames_types_codigo, exames_types_nome) in enumerate(exames_types):
            Exame.objects.create(
                nome=exames_types_nome,
                tipo_exame=random.choice(tipos_exames),
            )
                    
        self.stdout.write(self.style.SUCCESS('exames fake foram gerados com sucesso!'))
