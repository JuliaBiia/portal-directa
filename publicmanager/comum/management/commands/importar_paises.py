# -*- coding: utf-8 -*-
from django.db import transaction
from django.core.management.base import BaseCommand
import tqdm
import xlrd2

from publicmanager.comum.models import Pais


class Command(BaseCommand):
    help = 'Importação dos Países'

    def handle(self, *args, **options):
        ergon = xlrd2.open_workbook("publicmanager/comum/fixtures/paises.xls")  # arquivo de dados a ser importado
        pagina = ergon.sheet_by_index(0)

        with transaction.atomic():
            for i in tqdm.tqdm(range(1, pagina.nrows)):
                codigo_pais = str(pagina.cell_value(rowx=i, colx=0))
                nome_pais = str(pagina.cell_value(rowx=i, colx=1))
                try:
                    Pais.objects.get_or_create(codigo=codigo_pais, nome=nome_pais)
                except Exception as e:
                    print(e)
