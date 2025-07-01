import csv
import uuid
from django.core.management.base import BaseCommand

from publicmanager.saude.models import UnidadeSaude
from publicmanager.autenticacao.models import Usuario
from publicmanager.comum.models import Estado, Municipio
from publicmanager.saude_cadastro.models import Profissional

class Command(BaseCommand):
    help = 'Importação dos profissionais.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Gerando Importação dos profissionais...'))
        
        with open('publicmanager/saude/fixtures/profissionais.csv', newline='') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',')
            
            for row in spamreader:

                unidade_ids = [uuid.UUID(unidade_id.strip()) for unidade_id in row["Unidade de Saúde ID"].split(',')]
                unidades = UnidadeSaude.objects.filter(id__in=unidade_ids)

                estado = Estado.objects.get(estado=row['Estado'])
                municipio = Municipio.objects.get(nome=row['Municipio'])

                profissional, created = Profissional.objects.get_or_create(
                    defaults={'nome_profissional': row['Nome'],},
                    tipo_profissional = row['Tipo Profissional'],
                    coren = row['Coren'],
                    crm = row['CRM'],
                    cns = row['CNS'],
                    cbo = row['CBO'],
                    cpf = row['CPF'],
                    endereco = row['Endereco'],
                    numero = row['Numero'],
                    complemento = row['Complemento'],
                    bairro = row['Bairro'],
                    cep = row['CEP'],
                    estado = estado,
                    municipio = municipio,
                    telefone_1 = row['Telefone 1'],
                    telefone_2 = row['Telefone 2'],
                    email = row['E-mail'],
                    situacao = row['Situacao'],
                )

                cpf_replace = profissional.cpf.replace('.', '').replace('-', '')
                usuario = Usuario.objects.create_user(cpf_cnpj=cpf_replace, email=profissional.email, nome=profissional.nome_profissional, password=str(row['Senha']))
                usuario.password = row['Senha']
                usuario.save()
                
                profissional.unidades_saude.set(unidades)
                profissional.user = usuario
                profissional.save()


        self.stdout.write(self.style.SUCCESS('Importação dos profissionais gerados com sucesso!'))
