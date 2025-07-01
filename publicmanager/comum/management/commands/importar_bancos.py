# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from publicmanager.comum.models import Banco
import csv


class Command(BaseCommand):
    help = 'Importação dos bancos.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Gerando dados ...'))

        with open('publicmanager/comum/fixtures/bancos.csv', newline='') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',')
            for row in spamreader:
                try:
                    banco = Banco.objects.get(
                        ispb=row['ISPB'],
                        )
                    banco.nome_longo = row['Nome_Extenso']
                    banco.save()
                except:
                    Banco.objects.create(
                        ispb=row['ISPB'],
                        nome_longo=row['Nome_Extenso'],
                        nome_curto=row['Nome_Reduzido'],
                        codigo=row['Número_Código'],
                    )

        self.stdout.write(self.style.SUCCESS('Importação dos bancos gerados com sucesso!'))
