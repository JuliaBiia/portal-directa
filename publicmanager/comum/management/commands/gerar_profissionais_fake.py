import random
from faker import Faker
from django.core.management.base import BaseCommand
from publicmanager.autenticacao.models import Usuario
from publicmanager.saude.models import UnidadeSaude
from publicmanager.saude_cadastro.models import Profissional, Estado, Municipio

class Command(BaseCommand):
    help = 'Gerar Profissional inicial do sistema'

    def handle(self, *args, **options):
        fake = Faker()

        unidades_saude = UnidadeSaude.objects.filter(nome='UBS ZONA SUL').first()
        estados = Estado.objects.all()
        municipios = Municipio.objects.all()

        # List of profession types
        profissao_types = [
            ('DESENVOLVEDOR', 'DESENVOLVEDOR'),
            ('RECEPCIONISTA', 'RECEPCIONISTA'),
            ('MEDICO', 'MÉDICO'),
            ('ENFERMEIRO', 'ENFERMEIRO(A)'),
            ('RADIOLOGISTA', 'RADIOLOGISTA'),
            ('FARMACEUTICO', 'FARMACÊUTICO'),
            ('TERAPEUTA', 'TERAPEUTA'),
            ('NUTRICIONISTA', 'NUTRICIONISTA'),
            ('ADMINISTRADO', 'ADMINISTRADO'),
            ('SUPORTE', 'SUPORTE'),
        ]

        for index, (profissao_type_codigo, profissao_type_nome) in enumerate(profissao_types):

            profissional_nome = profissao_type_nome
            profissional_email = f'{profissao_type_nome}@gmail.com'
            profissional_password = f'123456789{index}'
            profissional_cpf = f'123456789{index}'

            profissional_user = Usuario.objects.create(
                cpf_cnpj=profissional_cpf,
                email=profissional_email,
                nome=profissional_nome,
            )
            profissional_user.set_password(profissional_password)
            profissional_user.save()

        
            profissional_data = {
                'nome_profissional': profissional_nome,
                'email': profissional_email,
                'tipo_profissional': index,
                'cpf': profissional_cpf,
                'endereco': f'Rua {fake.street_name()}',
                'numero': fake.building_number(),
                'complemento': fake.secondary_address(),
                'bairro': fake.word(),
                'cep': fake.zipcode(),
                'estado': random.choice(estados),
                'municipio': random.choice(municipios),
                'telefone_1': f'1234566543{index}',
                'situacao': 1,
            }

            profissional_instance = Profissional.objects.create(**profissional_data)
            profissional_instance.unidades_saude.set([unidades_saude])
            profissional_instance.user = profissional_user
            profissional_instance.save()