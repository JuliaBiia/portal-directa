# Generated by Django 4.2.10 on 2025-02-12 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saude_atendimento', '0020_medicacaoatendimento_estoque_zero_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicacaoatendimento',
            name='admin_medicamentosa',
            field=models.SmallIntegerField(choices=[(0, 'ORAL'), (1, 'PARENTAL'), (2, 'SUBCUTÂNIA'), (3, 'NASAL'), (4, 'RETAL'), (5, 'INTRAVESICAL'), (6, 'NEBOLIZAÇÃO'), (7, 'OCULAR'), (8, 'SUBLINGUAL'), (9, 'RESPIRATÓRIA'), (10, 'TÓPICO'), (11, 'DERMATOLÓGICA'), (12, 'INALATÓRIA'), (13, 'OTOLOGICA'), (14, 'TRANSDÉRMICA'), (15, 'VAGINAL'), (16, 'LOCAL'), (17, 'EPIDURAL')], verbose_name='Via de Administação Medicamentosa'),
        ),
    ]
