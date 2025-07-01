import random
from django.db import models
from django_lifecycle import hook
from publicmanager.comum.models import BaseModel
from django.template.defaultfilters import slugify
from smart_selects.db_fields import ChainedForeignKey
from simple_history.models import HistoricalRecords

from publicmanager.comum.models import BaseModel, Estado, Municipio

def manual_path(instance, filename):
    return f"manuais/{instance.pk}_{filename}"

def logo_upload_to(instance, filename):
    return f"unidade/logo/{instance}-{filename}"

class UnidadeSaude(BaseModel):
    nome = models.CharField(max_length=255)
    email = models.EmailField("Email do responsável", max_length=255)
    telefone = models.CharField("Telefone do responsável", max_length=15)
    logo = models.ImageField("Imagem", upload_to=logo_upload_to, blank=True, null=True, max_length=5000)
    
    ATIVO, DESATIVADO = range(2)
    SITUACAO_CHOICES = (
        (ATIVO, "Ativo"),
        (DESATIVADO, "Desativado"),
    )
    endereco = models.CharField('Endereço', max_length=255, help_text='Nome da rua, travessa ou avenida')
    cep = models.CharField(max_length=14, verbose_name="CEP", blank=True)
    situacao = models.SmallIntegerField("Situação", choices=SITUACAO_CHOICES, default=ATIVO)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)
    municipio = ChainedForeignKey(Municipio, on_delete=models.PROTECT, chained_field='estado', chained_model_field='estado', show_all=False, auto_choose=False)
    descricao = models.TextField('Descrição', blank=True)
    alta_atendimento = models.BooleanField('Faz alta no atendimento?', default=False)
    sigla = models.CharField('Sigla da unidade', max_length=10)
    slug = models.SlugField('Slug', null=False, unique=True, editable=False)
    cnes = models.CharField(max_length=255, blank=True, null=True)


    GERAL, URGENCIA, CONSULTORIO = range(3)
    TIPO_UNIDADE_CHOICES = (
         (GERAL, "GERAL"),
         (URGENCIA, "URGENCIA"),
         (CONSULTORIO, "CONSULTORIO")
     )
    tipo_unidade = models.SmallIntegerField("Tipo Unidade", choices=TIPO_UNIDADE_CHOICES, default=GERAL)

    class Meta:
        verbose_name = 'Unidade de Saúde'
        verbose_name_plural = 'Unidades de Saúde'

    def __str__(self):
        return f'{self.nome}'
    
    def formatar_nome_municipio(self):
        return self.municipio.nome.capitalize()
    
    @hook("before_save") 
    def create_slug(self):
        try:
            self.slug = slugify(self.nome)
        except Exception as e:
            self.slug = slugify(f'{self.nome}{random.randint(1, 50)}')
        
    @hook("before_create") 
    def create_classificacao_risco(self):
        from publicmanager.saude_cadastro.models import TipoClassificacaoRisco
        
        TIPO_CLASSIFICACAO_RISCO_CHOICES = (
            (TipoClassificacaoRisco.NAO_URGENTE, "NÃO URGENTE"),
            (TipoClassificacaoRisco.POUCO_URGENTE, "POUCO URGENTE"),
            (TipoClassificacaoRisco.URGENTE, 'URGENTE'),
            (TipoClassificacaoRisco.MUITO_URGENTE, 'MUITO URGENTE'),
            (TipoClassificacaoRisco.EMERGENTE, 'EMERGÊNCIA')
        )

        for index, (codigo, nome) in enumerate(TIPO_CLASSIFICACAO_RISCO_CHOICES):
            
            cor_classificacao = None
            if codigo == 0:
                cor_classificacao = TipoClassificacaoRisco.AZUL
            elif codigo == 1:
                cor_classificacao = TipoClassificacaoRisco.VERDE
            elif codigo == 2:
                cor_classificacao = TipoClassificacaoRisco.AMARELO
            elif codigo == 3:
                cor_classificacao = TipoClassificacaoRisco.LARANJA
            elif codigo == 4:
                cor_classificacao = TipoClassificacaoRisco.VERMELHO
                
            TipoClassificacaoRisco.objects.create(
                unidade_saude=self,
                tipo=codigo,
                ordem=index + 1,
                cor=cor_classificacao,
            )

class ResponsavelUnidade(BaseModel):
    unidade_saude = models.ForeignKey(UnidadeSaude, verbose_name='Unidade de Saúde',on_delete=models.PROTECT, null=True, blank=True)
    profissional = models.ForeignKey('saude_cadastro.Profissional', verbose_name='Profissional',on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Responsavel da Unidade'
        verbose_name_plural = 'Responsaveis das Unidades'

    def __str__(self):
        return f'{self.unidade_saude}'

class UnidadeLogin(BaseModel):
    profissional = models.OneToOneField('saude_cadastro.Profissional', on_delete=models.PROTECT)
    unidade = models.ForeignKey(UnidadeSaude, on_delete=models.PROTECT, null=True, blank=True)
    sala = models.ForeignKey('saude_cadastro.Sala', on_delete=models.PROTECT, null=True, blank=True)
    historico = HistoricalRecords()
    class Meta:
        verbose_name = 'Unidade logado'
        verbose_name_plural = 'Unidades Logado'

    def __str__(self):
        return f'{self.profissional} - {self.unidade}'
    
class Manual(BaseModel):
    nome = models.CharField(max_length=255)
    arquivo = models.FileField("Arquivo", upload_to=manual_path, blank=True, null=True)
    descricao = models.TextField("Descrição", blank=True, null=True)
    
    DESENVOLVEDOR, RECEPCIONISTA, MEDICO, ENFERMEIRO, RADIOLOGISTA, FARMACEUTICO, TERAPEUTA, \
    NUTRICIONISTA, ADMINISTRADO, SUPORTE = range(10)
    TIPO_CHOICES = [
        (DESENVOLVEDOR, 'DESENVOLVEDOR'),
        (RECEPCIONISTA, 'RECEPCIONISTA'),
        (MEDICO, 'MÉDICO'),
        (ENFERMEIRO, 'ENFERMEIRO(A)'),
        (RADIOLOGISTA, 'RADIOLOGISTA'),
        (FARMACEUTICO, 'FARMACÊUTICO'),
        (TERAPEUTA, 'TERAPEUTA'),
        (NUTRICIONISTA, 'NUTRICIONISTA'),
        (ADMINISTRADO, 'ADMINISTRADO'),
        (SUPORTE, 'SUPORTE'),
    ]
    tipo = models.SmallIntegerField(choices=TIPO_CHOICES)

    class Meta:
        verbose_name = 'Manual'
        verbose_name_plural = 'Manuais'

    def __str__(self):
        return f'{self.nome}'
    
class EsqueceuSenha(BaseModel):
    email = models.EmailField(verbose_name='E-mail')
    whatsapp = models.CharField(max_length=255)
    finalizado = models.BooleanField("Finalizado", default=False)

    class Meta:
        verbose_name = 'Esqueceu Senha'
        verbose_name_plural = 'Esqueceu Senhas'

    def __str__(self):
        return f'{self.email}'