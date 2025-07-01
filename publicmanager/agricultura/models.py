from django.db import models

class TipoProdutor(models.Model):
    descricao = models.CharField('Descrição', null=False, blank=False, max_length=100)

    class Meta:
        verbose_name = 'Tipo de Produtor'
        verbose_name_plural = 'Tipos de Produtores'

    def __str__(self):
        return f'[{self.codigo}] - {self.descricao}'
