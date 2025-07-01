import uuid
from django.db import models
from django_lifecycle import LifecycleModelMixin

class BaseModel(LifecycleModelMixin, models.Model):
	id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
	created_at  = models.DateTimeField(verbose_name='Registrado em', auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name='Atualizado em', auto_now=True)

	class Meta:
		abstract = True

class Estado(models.Model):
    estado = models.CharField(max_length=50)
    sigla = models.CharField(primary_key=True, unique=True, max_length=2)

    def __str__(self):
        return f'{self.estado}/{self.sigla}'
    
class Municipio(models.Model):
    SEARCH_FIELDS = ['ibge', 'nome', 'uf']

    ibge = models.CharField(unique=True, editable=True, max_length=7, primary_key=True,)
    nome = models.CharField(max_length=155)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Município'

    def __str__(self):
        return f'{self.nome}/{self.estado.sigla} - [{self.ibge}]'


class Nacionalidade:
    BRASILEIRO_NATO = 'Brasileiro Nato'
    BRASILEIRO_NATZ = 'Brasileiro Naturalizado'
    EQUIPARADO = 'Equiparado'
    ESTRANGEIRO = 'Estrangeiro'

    @classmethod
    def get_choices(cls):
        return [1, cls.BRASILEIRO_NATO], [2, cls.BRASILEIRO_NATZ], [3, cls.EQUIPARADO], [4, cls.ESTRANGEIRO]

class GrupoDeficiencia(models.Model):
    codigo = models.CharField('Código', null=False, blank=False, max_length=10)
    descricao = models.CharField('Descrição', null=False, blank=False, max_length=100)

    class Meta:
        verbose_name = 'Grupo de Deficiência'
        verbose_name_plural = 'Grupos de Deficiências'

    def __str__(self):
        return f'[{self.codigo}] - {self.descricao}'


class Deficiencia(models.Model):
    grupo_deficiencia = models.ForeignKey(GrupoDeficiencia, verbose_name='Grupo de Deficiência',
                                          on_delete=models.CASCADE)
    codigo = models.CharField('Código', null=False, blank=False, max_length=10)
    descricao = models.CharField('Descrição', null=False, blank=False, max_length=100)

    class Meta:
        verbose_name = 'Deficiência'
        verbose_name_plural = 'Deficiências'

    def __str__(self):
        return f'{self.grupo_deficiencia.descricao} - {self.descricao}'


class EstadoCivil(models.Model):
    nome = models.CharField(max_length=25)

    class Meta:
        verbose_name = 'Estado Civil'
        verbose_name_plural = 'Estados Civis'

    def __str__(self):
        return self.nome


class Banco(models.Model):
    ispb = models.CharField(max_length=8)
    codigo = models.CharField(max_length=3)
    nome_curto = models.CharField(max_length=70)
    nome_longo = models.CharField(max_length=150)

    def __str__(self):
        return self.nome_longo


class Pais(models.Model):
    codigo = models.CharField(max_length=4)
    nome = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Países'

    def __str__(self):
        return self.nome


class Raca(models.Model):
    SEARCH_FIELDS = ['descricao']
    descricao = models.CharField('Descrição', unique=True, max_length=55)

    class Meta:
        verbose_name = 'Raça'
        verbose_name_plural = 'Raças'

    def __str__(self):
        return self.descricao