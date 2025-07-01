import random
from faker import Faker
from django.core.management.base import BaseCommand

from publicmanager.saude.models import UnidadeSaude
from publicmanager.saude_cadastro.models import Profissao
from publicmanager.comum.models import Estado, Municipio
from publicmanager.saude_atendimento.models import Paciente

class Command(BaseCommand):
    help = 'Gerar dados fake para o cadastro de pacientes'

    def handle(self, *args, **options):
        fake = Faker('pt_BR')

        self.stdout.write(self.style.SUCCESS('Gerando dados ...'))
        estados = Estado.objects.all()
        municipios = Municipio.objects.all()
        profissoes = Profissao.objects.all()

        unidade_saude_types = [
            ('UBS_ZONA_SUL', 'UBS ZONA SUL'),
            ('UBS_ZONA_NORTE', 'UBS ZONA NORTE'),
            ('UBS_PIUM', 'UBS PIUM'),
            ('CENTRO_SAUDE', 'CENTRO DE SAÚDE DR ODILON GUEDES DA SILVA'),
            ('HOSPITAL_GISELDA_TRIGUEIRO', 'HOSPITAL GISELDA TRIGUEIRO'),
        ]

        for index, (unidade_type_code, unidade_type_name) in enumerate(unidade_saude_types):
            email_unidade = fake.email()

            unidade = UnidadeSaude.objects.create(
                nome=unidade_type_name,
                telefone=fake.unique.random_number(11),
                email=email_unidade,
                situacao=UnidadeSaude.ATIVO,
                estado=random.choice(estados),
                municipio=random.choice(municipios)
            )

            self.stdout.write(self.style.SUCCESS(f'Unidade criada: {unidade.nome}'))

        if not (estados and profissoes and municipios):
            self.stdout.write(self.style.ERROR('Um ou mais conjuntos de consultas estão vazios. Preencha as tabelas necessárias.'))
            return
        
        unidades = UnidadeSaude.objects.all()

        for _ in range(100):
            sexo = random.choice(['M', 'F'])
            
            # Gerar nome baseado no sexo escolhido
            if sexo == 'M':
                nome_paciente = ' '.join([fake.first_name_male(), fake.last_name(), fake.last_name()])
                nome_social = fake.first_name_male()
            else:
                nome_paciente = ' '.join([fake.first_name_female(), fake.last_name(), fake.last_name()])
                nome_social = fake.first_name_female()

            paciente_data = {
                'unidade_saude': random.choice(unidades),
                'nome_paciente': nome_paciente,
                'nome_social': nome_social,
                'cartao_sus': str(fake.unique.random_number(digits=15, fix_len=True)),
                'cpf': fake.ssn(),  # Gerar CPF válido
                'rg': fake.random_int(min=100000, max=999999),
                'situacao': 'ATIVO',

                'nome_mae': fake.name(),
                'data_nascimento': fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d'),
                'nacionalidade': 'Brasileiro',
                'sexo': sexo,
                'grau_de_instrucao': 'FUNDAMENTAL COMPLETO',
                'bairro': f'Bairro Teste {fake.unique.random_number(digits=5, fix_len=True)}',
                'endereco': f'Rua Teste {fake.unique.random_number(digits=5, fix_len=True)}',
               
                'estado': random.choice(estados),
                'profissao': random.choice(profissoes),
                'municipio': random.choice(municipios),
            }

            Paciente.objects.create(**paciente_data)

        self.stdout.write(self.style.SUCCESS('Dados fake gerados com sucesso!'))
