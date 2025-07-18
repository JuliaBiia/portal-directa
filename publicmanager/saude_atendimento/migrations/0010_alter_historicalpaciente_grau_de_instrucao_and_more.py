# Generated by Django 4.2.10 on 2024-07-10 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saude_atendimento', '0009_alter_historicalpaciente_numero_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpaciente',
            name='grau_de_instrucao',
            field=models.CharField(blank=True, choices=[['0', 'Creche'], ['1', 'PRÉ-ESCOLA (EXCETO CA)'], ['2', 'Classe de Alfabetização - CA'], ['3', 'Ensino Fundamental 1ª a 4ª séries, Elementar (Primário], Primeira fase do 1º grau'], ['4', 'Ensino Fundamental 5ª a 8ª séries, Médio 1º ciclo (Ginasial], Segunda fase do 1º grau '], ['5', 'Ensino Fundamental (duração 9 anos)'], ['6', ' Ensino Fundamental Especial'], ['7', ' Ensino Médio, 2º grau, Médio 2º ciclo (Científico, Clássico, Técnico, Normal) '], ['8', 'Ensino Médio Especial'], ['9', 'Ensino Fundamental EJA - séries iniciais (Supletivo 1ª a 4ª) '], ['10', ' Ensino Fundamental EJA - séries finais (Supletivo 5ª a 8ª) '], ['11', ' Ensino Médio EJA (Supletivo)'], ['12', 'Superior, Aperfeiçoamento, Especialização, Mestrado, Doutorado'], ['13', 'Alfabetização para Adultos (Mobral, etc.)'], ['14', 'Nenhum']], null=True, verbose_name='Grau de instrução'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='grau_de_instrucao',
            field=models.CharField(blank=True, choices=[['0', 'Creche'], ['1', 'PRÉ-ESCOLA (EXCETO CA)'], ['2', 'Classe de Alfabetização - CA'], ['3', 'Ensino Fundamental 1ª a 4ª séries, Elementar (Primário], Primeira fase do 1º grau'], ['4', 'Ensino Fundamental 5ª a 8ª séries, Médio 1º ciclo (Ginasial], Segunda fase do 1º grau '], ['5', 'Ensino Fundamental (duração 9 anos)'], ['6', ' Ensino Fundamental Especial'], ['7', ' Ensino Médio, 2º grau, Médio 2º ciclo (Científico, Clássico, Técnico, Normal) '], ['8', 'Ensino Médio Especial'], ['9', 'Ensino Fundamental EJA - séries iniciais (Supletivo 1ª a 4ª) '], ['10', ' Ensino Fundamental EJA - séries finais (Supletivo 5ª a 8ª) '], ['11', ' Ensino Médio EJA (Supletivo)'], ['12', 'Superior, Aperfeiçoamento, Especialização, Mestrado, Doutorado'], ['13', 'Alfabetização para Adultos (Mobral, etc.)'], ['14', 'Nenhum']], null=True, verbose_name='Grau de instrução'),
        ),
    ]
