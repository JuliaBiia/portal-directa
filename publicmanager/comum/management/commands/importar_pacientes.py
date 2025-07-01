import csv
import pytz
from datetime import datetime
from django.utils import timezone
from django.core.management.base import BaseCommand

from publicmanager.saude.models import UnidadeSaude
from publicmanager.saude_atendimento.models import Paciente, Estado, Municipio

class Command(BaseCommand):
    help = 'Importação dos Pacientes.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Importando Pacientes ...'))

        unidade = UnidadeSaude.objects.get(nome__exact="PRONTO ATENDIMENTO MUNICIPAL DOUTOR ODILON GUEDES")

        with open('publicmanager/comum/fixtures/producao/tb_pacientes.csv', newline='') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',')
            
            for row in spamreader:
                estado = Estado.objects.get(sigla=row['estado'])

                try:
                    municipio = Municipio.objects.get(ibge=row['municipio'])
                except Municipio.DoesNotExist:
                    print(f"Município com o IBGE {row['municipio']} não encontrado.")
                    municipio=None

                try:
                    if row['created_at']:
                        created_at = datetime.strptime(row['created_at'], "%Y-%m-%d %H:%M:%S")
                        if timezone.is_naive(created_at):
                            created_at = timezone.make_aware(created_at, timezone.get_default_timezone())
                    else:
                        created_at = None

                    if row['updated_at']:
                        updated_at = datetime.strptime(row['updated_at'], "%Y-%m-%d %H:%M:%S")
                        if timezone.is_naive(updated_at):
                            updated_at = timezone.make_aware(updated_at, timezone.get_default_timezone())
                    else:
                        updated_at = None
                    
                    if row['data_nascimento']:
                        data_nascimento = datetime.strptime(row['data_nascimento'], "%Y-%m-%d").date()
                    else:
                        data_nascimento = None
                    
                    if row['rg_data']:
                        rg_data = datetime.strptime(row['rg_data'], "%Y-%m-%d").date()
                    else:
                        rg_data = None

                    if row['cpf']:
                        cpf = row['cpf']
                    else:
                        cpf = None


                    Paciente.objects.get_or_create(
                        unidade_saude=unidade,
                        updated_at=updated_at,
                        created_at=created_at,
                        endereco=row['endereco'],
                        numero=int(row['numero']) if row['numero'] else None,
                        complemento=row['complemento'],
                        cep=row['cep'],
                        nome_responsavel_1=row['nome_responsavel_1 no_entrevistador_fam'],
                        cpf_responsavel_1=row['cpf_responsavel_1'],
                        nome_paciente=row['nome_paciente'],
                        nome_social=row['nome_social'],
                        sexo=row['sexo'],
                        data_nascimento=data_nascimento,
                        nome_mae=row['nome_mae'],
                        nome_pai=row['nome_pai'],
                        estado=estado,
                        municipio=municipio,
                        cpf=cpf,
                        rg=row['rg'],
                        rg_data=rg_data,
                        rg_orgao=row['rg_orgao'],
                    )
                except Exception as e:
                    print(e)

        self.stdout.write(self.style.SUCCESS('Importação dos pacientes gerados com sucesso!'))