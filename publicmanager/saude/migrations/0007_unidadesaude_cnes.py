# Generated by Django 4.2.10 on 2024-10-19 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saude', '0006_unidadesaude_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='unidadesaude',
            name='cnes',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
