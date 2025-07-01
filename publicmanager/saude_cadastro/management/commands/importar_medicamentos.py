# -*- coding: utf-8 -*-
from django.db import transaction
from django.core.management.base import BaseCommand
import tqdm
import xlrd2

from publicmanager.saude_farmacia.models import Medicamento

class Command(BaseCommand):
    help = 'Importação dos Medicamentos'

    def handle(self, *args, **options):
        ergon = xlrd2.open_workbook("publicmanager/saude/fixtures/medicamentos_base_horus.xlsx")  # arquivo de dados a ser importado

        for index in range(0,3):
            pagina = ergon.sheet_by_index(index)

            with transaction.atomic():
                for i in tqdm.tqdm(range(1, pagina.nrows)):
                    descricao_medicamento = str(pagina.cell_value(rowx=i, colx=0))
                    codigo_medicamento = str(pagina.cell_value(rowx=i, colx=1))
                    try:
                        Medicamento.objects.get_or_create(
                            descricao=descricao_medicamento,
                            codigo=codigo_medicamento,
                            tipo_medicamento=index+1
                        )
                    except Exception as e:
                        print(e)

        
