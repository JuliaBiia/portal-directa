
from faker import Faker
from django.db import transaction
from django.utils.translation import gettext as _
from django.core.management.base import BaseCommand
from publicmanager.saude_cadastro.models import UnidadeSaude, Sala, UnidadeSetor

class Command(BaseCommand):
    help = 'Gerar setores e salas fake para teste de sistema'

    def handle(self, *args, **kwargs):
        fake = Faker('pt_BR')

        try:
            self.stdout.write(self.style.SUCCESS(_('Generating data...')))

            with transaction.atomic():
                unidades = UnidadeSaude.objects.all()

                for unidade in unidades:
                    setores_types = [
                        (1, 'URG', 'URGENCIA', 'URGÊNCIA'),
                        (2, 'CON', 'CONSULTORIO', 'CONSULTÓRIO'),
                        (3, 'ENF', 'ENFERMARIA', 'ENFERMARIA'),
                        (7, 'LAB', 'LABORATORIO', 'LABORATÓRIO'),
                        (12, 'RAD', 'RADIOLOGIA', 'RADIOLOGIA'),
                    ]

                    setores_to_create = []
                    for tipo, code, setor_type_code, setor_type_name in setores_types:
                        setores_to_create.append(UnidadeSetor(
                            nome=setor_type_name,
                            unidade_saude=unidade,
                            codigo=fake.unique.random_number(6),
                            sigla=code,
                            tipo=tipo
                        ))
                    
                    UnidadeSetor.objects.bulk_create(setores_to_create)

                    setores = UnidadeSetor.objects.filter(unidade_saude=unidade).order_by('nome')

                    salas_to_create = []
                    for setor in setores:
                        for index in range(5):
                            salas_to_create.append(Sala(
                                unidade_setor=setor,
                                nome_sala=f'{setor.sigla}{index}'
                            ))

                    Sala.objects.bulk_create(salas_to_create)

            self.stdout.write(self.style.SUCCESS(_('Salas geradas com sucesso!')))
        except Exception as e:
            self.stderr.write(self.style.ERROR(_('Ocorreu um erro: %s' % str(e))))