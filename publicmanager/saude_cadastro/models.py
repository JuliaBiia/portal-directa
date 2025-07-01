from django.db import models
from django_lifecycle import hook
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator
from smart_selects.db_fields import ChainedForeignKey

from publicmanager.saude.models import UnidadeSaude
from publicmanager.autenticacao.models import Usuario
from publicmanager.comum.models import BaseModel, Estado, Municipio

class UnidadeSetor(BaseModel):
    nome = models.CharField(max_length=100)
    unidade_saude = models.ForeignKey(UnidadeSaude, verbose_name='Unidade de Saúde',on_delete=models.PROTECT, null=True, blank=True)
    codigo = models.CharField('Código', max_length=10, unique=True, blank=True, null=True)
    superior = models.ForeignKey('self', null=True, blank=True, verbose_name='Unidade Superior', on_delete=models.PROTECT)
    ATIVO, INATIVADO = range(2)
    SITUACAO_CHOICES = (
         (ATIVO, "Ativo"),
         (INATIVADO, "Inativado"),
     )
    situacao = models.SmallIntegerField("Situação", choices=SITUACAO_CHOICES, default=ATIVO)
    sigla = models.CharField('Sigla', max_length=15, blank=True, null=True)
    recebe_paciente = models.BooleanField(verbose_name='Recebe paciente', default=False)

    RECEPCAO, URGENCIA, CONSULTORIO, ENFERMARIA, INTERNACAO, FARMACIA, NUTRICAO, LABORATORIO, \
    CENTRO_CIRURGICO, MATERNIDADE, OBSTRETICIA, PEDIATRIA, RADIOLOGIA, RH, ADMINISTRATIVO, CLASSIFICACAO_RISCO  = range(16)
    TIPO_CHOICES = (
        (RECEPCAO, "RECEPÇÃO"),
        (URGENCIA, "URGÊNCIA"),
        (CONSULTORIO, "CONSULTÓRIO"),
        (ENFERMARIA, "ENFERMARIA"),
        (INTERNACAO, "INTERNAÇÃO"),
        (FARMACIA, "FARMACIA"),
        (NUTRICAO, "NUTRIÇÃO"),
        (LABORATORIO, "LABORATÓRIO"),
        (CENTRO_CIRURGICO, "CENTRO CIRÚRGICO"),
        (MATERNIDADE, "MATERNIDADE"),
        (OBSTRETICIA, "OBSTRETICIA"),
        (PEDIATRIA, "PEDIATRIA"),
        (RADIOLOGIA, "RADIOLOGIA"),
        (RH, "RH"),
        (ADMINISTRATIVO, "ADMINISTRATIVO"),
        (CLASSIFICACAO_RISCO, "CLASSIFICAÇÃO DE RISCO"),
    )
    tipo = models.SmallIntegerField("Tipo", choices=TIPO_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name = 'Unidade Setor'
        verbose_name_plural = 'Unidades setores'

    def __str__(self):
        return f'{self.nome} - {self.unidade_saude}'
    
class TipoClinica(BaseModel):
    descricao = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Tipo Clinica'
        verbose_name_plural = 'Tipo Clinica'

    def __str__(self):
        return self.descricao

class Convenio(BaseModel):
    nome = models.CharField('Nome', unique=True, max_length=50)

    class Meta:
        verbose_name = 'Convênio'
        verbose_name_plural = 'Convênios'

    def __str__(self):
        return self.nome

class CID(BaseModel):
    codigo = models.CharField(max_length=20)
    nome = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'CID'
        verbose_name_plural = 'CIDs'

    def __str__(self):
        return self.nome

class DestinoObito(BaseModel):
    ATIVO = 'ATIVO'
    INATIVO = 'INATIVO'
    SITUACOES_CHOICES = [
        (ATIVO, 'ATIVO'),
        (INATIVO, 'INATIVO'),
    ]

    unidade_saude = models.ForeignKey(UnidadeSaude, verbose_name='Unidade de Saúde',on_delete=models.PROTECT, null=True, blank=True)
    nome_destino_obito = models.CharField('Destino de Óbito', max_length=50)
    situacao = models.CharField('Situação', max_length=7, choices=SITUACOES_CHOICES, default=ATIVO)

    class Meta:
        verbose_name = 'Destino de Óbito'
        verbose_name_plural = 'Destinos de Óbito'

    def __str__(self):
        return self.nome_destino_obito

class TipoExame(BaseModel):
    nome = models.CharField('Nome', unique=True, max_length=150)
    
    LABORATORIO, IMAGEM = range(2)
    TIPO_CHOICES = (
        (LABORATORIO, "LABORATÓRIO"),
        (IMAGEM, "IMAGEM"),
    )
    tipo = models.SmallIntegerField("Tipo", choices=TIPO_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name = 'Tipo de Exames'
        verbose_name_plural = 'Tipos de Exames'

    def __str__(self):
        return self.nome
    
class TipoClassificacaoRisco(BaseModel):
    unidade_saude = models.ForeignKey(UnidadeSaude, verbose_name='Unidade de Saúde',on_delete=models.PROTECT, null=True, blank=True)
    
    NAO_URGENTE, POUCO_URGENTE, URGENTE, MUITO_URGENTE, EMERGENTE = range(5)
    TIPO_CLASSIFICACAO_RISCO_CHOICES = (
        (NAO_URGENTE, "NÃO URGENTE"),
        (POUCO_URGENTE, "POUCO URGENTE"),
        (URGENTE, 'URGENTE'),
        (MUITO_URGENTE, 'MUITO URGENTE'),
        (EMERGENTE, 'EMERGÊNCIA')
    )
    tipo = models.SmallIntegerField("Tipo de Classificacao de Risco", choices=TIPO_CLASSIFICACAO_RISCO_CHOICES)
    
    AZUL, VERDE, AMARELO, VERMELHO, LARANJA, PRETO, ROXO, CINZA = range(8)
    COR_CHOICES = (
        (AZUL, "AZUL"),
        (VERDE, "VERDE"),
        (AMARELO, 'AMARELO'),
        (VERMELHO, 'VERMELHO'),
        (LARANJA, 'LARANJA'),
        (PRETO, 'PRETO'),
        (ROXO, 'ROXO'),
        (CINZA, 'CINZA'),
    )
    cor = models.SmallIntegerField("Cor da Classificação", choices=COR_CHOICES, null=True)
    
    ATIVO, INATIVO = range(2)
    SITUACAO_CHOICES = (
        (ATIVO, "ATIVO"),
        (INATIVO, "INATIVO"),
    )
    situacao = models.SmallIntegerField("Situação", choices=SITUACAO_CHOICES, default=ATIVO)
    ordem = models.IntegerField('Ordem')
    tempo_atendimento = models.DurationField("Tempo para atendimento", blank=True, null=True)

    class Meta:
        verbose_name = 'Tipo de Classificação de Risco'
        verbose_name_plural = 'Tipos de Classificações de Risco'

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.unidade_saude}'

class Exame(BaseModel):
    nome = models.CharField('Exame', max_length=150)
    tipo_exame = models.ForeignKey(TipoExame, verbose_name='Tipo de Exames',on_delete=models.PROTECT)
    removido_sistema = models.BooleanField('Removido do sistema?', default=False)

    class Meta:
        verbose_name = 'Exame'
        verbose_name_plural = 'Exames'

    def __str__(self):
        return self.nome

class TipoHistoriaClinica(BaseModel):
    ATIVO = 'ATIVO'
    INATIVO = 'INATIVO'
    SITUACOES_CHOICES = [
        (ATIVO, 'ATIVO'),
        (INATIVO, 'INATIVO'),
    ]

    nome = models.CharField('Nome', unique=True, max_length=50)
    situacao = models.CharField('Situação', max_length=7, choices=SITUACOES_CHOICES, default=ATIVO)

    class Meta:
        verbose_name = 'Tipos de História Clínica'
        verbose_name_plural = 'Tipo de História Clínica'

    def __str__(self):
        return self.situacao

class TipoPosologia(BaseModel):
    nome = models.CharField('Nome', unique=True, max_length=50)
    quantidade = models.IntegerField('Quantidade')
    antes_da_refeicao = models.BooleanField("Antes da refeição", default=False)
    pos_refeicao = models.BooleanField("Pós refeição", default=False)
    somente_nas_refeicoes = models.BooleanField("Somente nas refeições", default=False)

    class Meta:
        verbose_name = 'Tipos de Posologia'
        verbose_name_plural = 'Tipo de Posologia'

    def __str__(self):
        return self.nome

class Transporte(BaseModel):
    ATIVO = 'ATIVO'
    INATIVO = 'INATIVO'
    SITUACOES_CHOICES = [
        (ATIVO, 'ATIVO'),
        (INATIVO, 'INATIVO'),
    ]

    nome_transporte = models.CharField('Nome do transporte', unique=True, max_length=50)
    situacao = models.CharField('Situação', max_length=7, choices=SITUACOES_CHOICES, default=ATIVO)

    class Meta:
        verbose_name = 'Transporte'
        verbose_name_plural = 'Transportes'

    def __str__(self):
        return self.nome_transporte

class Sala(BaseModel):
    unidade_setor = models.ForeignKey(UnidadeSetor, verbose_name='Unidade Setor',on_delete=models.PROTECT)
    nome_sala = models.CharField('Nome da sala', max_length=50)
    ATIVO, INATIVO, INDISPONIVEL, MANUTENCAO  = range(4)
    SITUACAO_CHOICES = [
        (ATIVO, 'Ativo'),
        (INATIVO, 'Inativo'),
        (INDISPONIVEL, 'Indisponível'),
        (MANUTENCAO, 'Manutenção')
    ]
    situacao = models.SmallIntegerField("Situação", choices=SITUACAO_CHOICES, default=ATIVO)

    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'

    def __str__(self):
        return f'{self.nome_sala} - {self.unidade_setor.nome}'

class Procedimento(BaseModel):
    nome = models.CharField('Nome', unique=True, max_length=255)
    codigo = models.CharField('Codigo', unique=True, max_length=20)

    class Meta:
        verbose_name = 'Procedimento'
        verbose_name_plural = 'Procedimentos'

    def __str__(self):
        return f'{self.nome}'

class Profissional(BaseModel):
    user = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.PROTECT)
    nome_profissional = models.CharField('Nome do Profissional', max_length=100, help_text='Nome do profissional')
    unidades_saude = models.ManyToManyField(UnidadeSaude, verbose_name='Unidades de Saúde')
    
    DESENVOLVEDOR, RECEPCIONISTA, MEDICO, ENFERMEIRO, RADIOLOGISTA, FARMACEUTICO, TERAPEUTA, \
    NUTRICIONISTA, ADMINISTRADO, SUPORTE, TECNICO_ENFERMAGEM = range(11)
    TIPO_PROFISSIONAL_CHOICES = [
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
        (TECNICO_ENFERMAGEM, 'TECNICO DE ENFERMAGEM'),
    ]

    tipo_profissional = models.SmallIntegerField(choices=TIPO_PROFISSIONAL_CHOICES)
    coren = models.CharField('COREN', max_length=7, blank=True, help_text='COREN')
    cofen = models.CharField('COFEN', max_length=7, blank=True, help_text='COFEN')
    crm = models.CharField('CRM', max_length=6, blank=True, help_text='CRM')
    cns = models.CharField('CNS', max_length=15, blank=True, help_text='CNS')
    cbo = models.CharField('CBO', max_length=6, blank=True, help_text='CBO')
    cpf = models.CharField(max_length=14, verbose_name="CPF", unique=True, error_messages={'unique': 'Um profissional com esse CPF já foi cadastrado.'})
    endereco = models.CharField('Endereço', max_length=200, help_text='Nome da rua, travessa ou avenida')
    numero = models.PositiveIntegerField('Número', blank=True, null=True,  help_text='Número', validators=[MaxValueValidator(9999999999999)])
    complemento = models.CharField('Complemento', blank=True,  max_length=200, help_text='Complemento torre, sala etc')
    bairro = models.CharField('Bairro', max_length=200, help_text='Nome do barro')
    cep = models.CharField(max_length=14, verbose_name="CEP", blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    municipio = ChainedForeignKey(Municipio, on_delete=models.CASCADE, chained_field='estado', chained_model_field='estado', show_all=False, auto_choose=False)
    telefone_1 = models.CharField('Telefone 1', max_length=15, unique=True, error_messages={'unique': 'Este número de telefone já está associado a uma conta existente.'}, help_text='Telefone 1')
    telefone_2 = models.CharField('Telefone 2', max_length=15, error_messages={'unique': 'Este número de telefone já está associado a uma conta existente.'}, blank=True, help_text='Telefone 2')
    email = models.EmailField(blank=True, verbose_name='E-mail', unique=True, error_messages={'unique': 'Uma email idêntico já foi cadastrado.'})
    situacao = models.CharField('Situação', max_length=7, choices=[['ATIVO', 'ATIVO'], ['INATIVO', 'INATIVO']], default='ATIVO')
    recepcao_noturno = models.BooleanField('Faz admissão noturna de pacientes?', default=False)
    class Meta:
        verbose_name = 'Profissional'
        verbose_name_plural = 'Profissionais'

    def __str__(self):
        return f'{self.nome_profissional} CRM: {self.crm}'
        
class Profissao(BaseModel):
    codigo = models.CharField('Código da profissão', unique=True, max_length=6)
    titulo = models.CharField('Título da profissão', max_length=150)

    class Meta:
        verbose_name = 'Profissão'
        verbose_name_plural = 'Profissões'

    def __str__(self):
        return self.titulo
    
class PainelChamada(BaseModel):
    nome = models.CharField('Nome', max_length=100)
    unidade_saude = models.ForeignKey(UnidadeSaude, verbose_name='Unidade de Saúde', on_delete=models.PROTECT, null=True, blank=True)
    setores = models.ManyToManyField(UnidadeSetor, verbose_name='Setores')
    slug = models.SlugField('Slug', null=False, unique=True, editable=False)

    class Meta:
        verbose_name = 'Painel Chamado'
        verbose_name_plural = 'Paineis de Chamados'

    def __str__(self):
        return f'{self.nome}'
    
    @hook("before_save") 
    def create_slug(self):

        if not self.slug:
            self.slug = slugify(self.nome)
