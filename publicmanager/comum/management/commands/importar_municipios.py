# -*- coding: utf-8 -*-
from django.db import transaction
from django.core.management.base import BaseCommand
import tqdm
import xlrd2

from publicmanager.comum.models import Municipio, Estado



class Command(BaseCommand):
    help = 'Importação dos Países'

    def handle(self, *args, **options):
        planilha = xlrd2.open_workbook("publicmanager/comum/fixtures/municipios.xlsx")  # arquivo de dados a ser importado
        pagina = planilha.sheet_by_index(0)

        ESTADOS = {
            'AC': 'Acre',
            'AL': 'Alagoas',
            'AP': 'Amapá',
            'AM': 'Amazonas',
            'BA': 'Bahia',
            'CE': 'Ceará',
            'DF': 'Distrito Federal',
            'ES': 'Espírito Santo',
            'GO': 'Goiás',
            'MA': 'Maranhão',
            'MT': 'Mato Grosso',
            'MS': 'Mato Grosso do Sul',
            'MG': 'Minas Gerais',
            'PA': 'Pará',
            'PB': 'Paraíba',
            'PR': 'Paraná',
            'PE': 'Pernambuco',
            'PI': 'Piauí',
            'RJ': 'Rio de Janeiro',
            'RN': 'Rio Grande do Norte',
            'RS': 'Rio Grande do Sul',
            'RO': 'Rondônia',
            'RR': 'Roraima',
            'SC': 'Santa Catarina',
            'SP': 'São Paulo',
            'SE': 'Sergipe',
            'TO': 'Tocantins',
        }    
        with transaction.atomic():
            for i in tqdm.tqdm(range(1, pagina.nrows)):
                ibge_municipio = str(pagina.cell_value(rowx=i, colx=0))
                nome_municipio = str(pagina.cell_value(rowx=i, colx=1))
                uf_estado_municipio = str(pagina.cell_value(rowx=i, colx= 2))
                try:
                    nome_estado_municipio = ESTADOS[uf_estado_municipio]
                    estado = Estado.objects.get_or_create(estado=nome_estado_municipio, sigla=uf_estado_municipio)[0]
                    Municipio.objects.get_or_create(ibge=ibge_municipio, nome=nome_municipio, estado=estado)
                    
                except Exception as e:
                    print(e)