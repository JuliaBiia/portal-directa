from django_lifecycle import hook
from django.db import models
from simple_history.models import HistoricalRecords
from publicmanager.comum.models import BaseModel

UNIDADE_CHOICES = (('Unidade', 'Unidade'),('Caixa', 'Caixa'),)

class Farmacia(BaseModel):
    CENTRAL, SETORIAL = range(2)
    TIPO_FARMACIA_CHOICES = [
        (CENTRAL, 'CENTRAL'),
        (SETORIAL, 'SETORIAL'),
    ]

    ATIVO, INATIVO = range(2)
    SITUACAO_CHOICES = (
        (ATIVO, "ATIVO"),
        (INATIVO, "INATIVO"),
    )

    unidade_saude = models.ForeignKey('saude.UnidadeSaude', verbose_name='Unidade de saúde', null=True, blank=True,on_delete=models.PROTECT)
    setor = models.ForeignKey('saude_cadastro.UnidadeSetor', verbose_name='Setor', on_delete=models.PROTECT)
    farmacia_superior = models.ForeignKey('self', null=True, blank=True, verbose_name='Farmácia Superior', on_delete=models.PROTECT)


    nome_farmacia = models.CharField('Nome', unique=True, error_messages={'unique': 'Uma farmácia com esse nome já existe.'}, max_length=200)
    tipo_farmacia = models.IntegerField('Tipo da farmácia', choices=TIPO_FARMACIA_CHOICES, default=CENTRAL)
    situacao_farmacia = models.SmallIntegerField('Situação', choices=SITUACAO_CHOICES, default=ATIVO)

    historico = HistoricalRecords()
    class Meta:
        verbose_name = 'Farmácia'
        verbose_name_plural = 'Farmácias'

    def __str__(self):
        return f'{self.nome_farmacia} - Unidade: {self.unidade_saude}'

class Produto(BaseModel):

    PRODUTO_MEDICO_ATIVO,PRODUTO_MEDICO_ATIVO_PARA_DIAGNOSTICO,PRODUTO_MEDICO_ATIVO_PARA_TERAPIA,PRODUTO_MEDICO_DE_USO_UNICO,PRODUTO_MEDICO_IMPLANTAVEL,PRODUTO_MEDICO_INVASIVO,PRODUTO_MEDICO_INVASIVO_CIRURGICAMENTE,PRODUTO_PARA_DIAGNOSTICO_IN_VITRO = range(8)
    TIPO_PRODUTO_CHOICES = [
        (PRODUTO_MEDICO_ATIVO, "PRODUTO MÉDICO ATIVO"),
        (PRODUTO_MEDICO_ATIVO_PARA_DIAGNOSTICO, "PRODUTO MÉDICO ATIVO PARA DIAGNÓSTICO"),
        (PRODUTO_MEDICO_ATIVO_PARA_TERAPIA, "PRODUTO MÉDICO ATIVO PARA TERAPIA"),
        (PRODUTO_MEDICO_DE_USO_UNICO, "PRODUTO MÉDICO DE USO ÚNICO"),
        (PRODUTO_MEDICO_IMPLANTAVEL, "PRODUTO MÉDICO IMPLANTÁVEL"),
        (PRODUTO_MEDICO_INVASIVO, "PRODUTO MÉDICO INVASIVO"),
        (PRODUTO_MEDICO_INVASIVO_CIRURGICAMENTE, "PRODUTO MÉDICO INVASIVO CIRURGICAMENTE"),
        (PRODUTO_PARA_DIAGNOSTICO_IN_VITRO, "PRODUTO PARA DIAGNÓSTICO IN VITRO"),
    ]

    ATIVO, INATIVO = range(2)
    SITUACAO_CHOICES = (
        (ATIVO, "ATIVO"),
        (INATIVO, "INATIVO"),
    )


    unidade_saude = models.ForeignKey('saude.UnidadeSaude', verbose_name='Unidade de saúde', null=True, blank=True, on_delete=models.PROTECT)
    
    nome_produto = models.CharField('Nome', max_length=200, unique=True, error_messages={'unique': 'Um produto com esse nome já existe.'})
    codigo_de_barra = models.CharField('Código de barra', max_length=50, unique=True, error_messages={'unique': 'Um produto com esse código de barra já existe. '})
    descricao_produto = models.TextField('Descrição', blank=True)

    tipo_produto = models.IntegerField('Tipo do produto', choices=TIPO_PRODUTO_CHOICES, default=PRODUTO_MEDICO_ATIVO)
    
    estoque_minimo_geral = models.PositiveIntegerField('Estoque mínimo geral')
    quantidade = models.PositiveIntegerField('Quantidade', default=0)
    
    situacao_produto = models.SmallIntegerField('Situação', choices=SITUACAO_CHOICES, default=ATIVO)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = 'Produtos'
    
    def __str__(self):
        return f'{self.nome_produto} - Tipo do produto: {self.tipo_produto}'


class PrincipioAtivo(BaseModel):
    nome = models.CharField('Nome', unique=True, max_length=255)

    class Meta:
        verbose_name = 'Princípio Ativo'
        verbose_name_plural = 'Princípios Ativos'

    def __str__(self):
        return self.nome

class Medicamento(BaseModel):
    COD_SUS, LICITACAO, AVULSO = range(3)
    TIPO_MEDICAMENTO_CHOICES = [
        (COD_SUS, 'COD SUS'),
        (LICITACAO, 'LICITAÇÃO'),
        (AVULSO, 'AVULSO'),
    ]

    ATIVO, INATIVO = range(2)
    SITUACAO_CHOICES = (
        (ATIVO, "ATIVO"),
        (INATIVO, "INATIVO"),
    )

    unidade_saude = models.ForeignKey('saude.UnidadeSaude', verbose_name='Unidade de saúde', null=True, blank=True, on_delete=models.PROTECT)

    nome_medicamento = models.CharField('Nome', max_length=200, null=True, blank=True)
    codigo_de_barra = models.CharField('Código de barra', max_length=50, unique=True, error_messages={'unique': 'Um medicamento com esse código de barra já existe. '}, null=True, blank=True)
    descricao_medicamento = models.TextField('Descrição', blank=True)
    
    principio_ativo_medicamento = models.ForeignKey(PrincipioAtivo, verbose_name='Princípio ativo do medicamento', on_delete=models.PROTECT, null=True, blank=True)
    
    tipo_medicamento = models.IntegerField(choices=TIPO_MEDICAMENTO_CHOICES, default=COD_SUS, null=True, blank=True)

    estoque_minimo_geral = models.PositiveIntegerField('Estoque mínimo geral', null=True, blank=True)
    quantidade = models.IntegerField('Quantidade', default=0)

    situacao_medicamento = models.SmallIntegerField('Situação', choices=SITUACAO_CHOICES, default=ATIVO)

    class Meta:
        verbose_name = 'Medicamento'
        verbose_name_plural = 'Medicamentos'

    def __str__(self):
        return f'{self.nome_medicamento} - Tipo de medicamento: {self.tipo_medicamento}'

class Insumo(BaseModel):
    ATIVO, INATIVO = range(2)
    SITUACAO_CHOICES = (
        (ATIVO, "ATIVO"),
        (INATIVO, "INATIVO"),
    )

    unidade_saude = models.ForeignKey('saude.UnidadeSaude', verbose_name='Unidade de saúde', null=True, blank=True, on_delete=models.PROTECT)

    nome_insumo = models.CharField('Nome', max_length=200, unique=True, null=True, error_messages={'unique': 'Um insumo com esse nome já existe.'})
    codigo_de_barra = models.CharField('Código de barra', max_length=50, unique=True, null=True, error_messages={'unique': 'Um insumo com esse código de barra já existe. '})
    descricao_insumo = models.TextField('Descrição', blank=True)

    estoque_minimo_geral = models.PositiveIntegerField('Estoque mínimo geral', null=True)
    quantidade = models.PositiveIntegerField('Quantidade', default=0)

    situacao_insumo = models.SmallIntegerField('Situação', choices=SITUACAO_CHOICES, default=ATIVO)


    def __str__(self):
        return f'{self.nome_insumo}'


class InsumoRequisitado(BaseModel):
    unidade_saude = models.ForeignKey('saude.UnidadeSaude', verbose_name='Unidade de saúde', null=True, blank=True, on_delete=models.PROTECT)

    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, blank=True)
    quantidade_insumo = models.IntegerField(blank=True)
    unidade_insumo = models.CharField(max_length=7, choices=UNIDADE_CHOICES, blank=True)

    def __str__(self):
        return self.insumo.nome_insumo

class MedicamentoRequisitado(BaseModel):
    unidade_saude = models.ForeignKey('saude.UnidadeSaude', verbose_name='Unidade de saúde', null=True, blank=True, on_delete=models.PROTECT)

    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, blank=True)
    quantidade_medicamento = models.IntegerField(blank=True)
    unidade_medicamento = models.CharField(max_length=7, choices=UNIDADE_CHOICES, blank=True)

    def __str__(self):
        return self.medicamento.nome_medicamento

class ProdutoRequisitado(BaseModel):
    unidade_saude = models.ForeignKey('saude.UnidadeSaude', verbose_name='Unidade de saúde', null=True, blank=True, on_delete=models.PROTECT)

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, blank=True)
    quantidade_produto = models.IntegerField(blank=True)
    unidade_produto = models.CharField(max_length=7, choices=UNIDADE_CHOICES, blank=True)

    def __str__(self):
        return self.produto.nome_produto

class RequisicaoMaterialFarmacia(BaseModel):
    SOLICITADO, DEFERIDO, CONCLUIDO, REJEITADO = range(4)
    TIPO_SITUACAO_CHOICES = [
        (SOLICITADO, 'SOLICITADO'),
        (DEFERIDO, 'DEFERIDO'),
        (CONCLUIDO, 'CONCLUÍDO'),
        (REJEITADO, 'REJEITADO'),
    ]

    unidade_saude = models.ForeignKey('saude.UnidadeSaude', verbose_name='Unidade de saúde', null=True, blank=True, on_delete=models.PROTECT)

    numero_pedido = models.CharField(max_length=12)
    farmaceutico_solicitante = models.ForeignKey('saude_cadastro.Profissional', on_delete=models.PROTECT, blank=True, null=True)
    data_solicitacao = models.DateTimeField(auto_now=True)
    data_entrada = models.DateTimeField(blank=True, null=True)
    farmacia = models.ForeignKey(Farmacia, on_delete=models.PROTECT)

    insumo_requisitado = models.ManyToManyField(InsumoRequisitado, blank=True)
    medicamento_requisitado = models.ManyToManyField(MedicamentoRequisitado, blank=True)
    produto_requisitado = models.ManyToManyField(ProdutoRequisitado, blank=True)

    situacao_requisicao = models.IntegerField(choices=TIPO_SITUACAO_CHOICES, default=SOLICITADO)

    def __str__(self):
        return f'{self.numero_pedido} - Data da solicitação: {self.data_solicitacao} - Farmácia: {self.farmacia}'


class InsumoEntrada(BaseModel):
    unidade_saude = models.ForeignKey('saude.UnidadeSaude', verbose_name='Unidade de saúde', null=True, blank=True, on_delete=models.PROTECT)

    insumo = models.ForeignKey(Insumo, on_delete=models.PROTECT, blank=True)
    quantidade_insumo = models.IntegerField(blank=True)
    unidade_insumo = models.CharField(max_length=7, choices=UNIDADE_CHOICES, blank=True)
    numero_lote_insumo = models.CharField(max_length=50)
    data_vencimento_insumo = models.DateField()

    def __str__(self):
        return self.insumo.nome_insumo
    
    @hook("after_create")
    def incrementar_quantidade_insumo(self):
        self.insumo.quantidade += int(self.quantidade_insumo)
        self.insumo.codigo_de_barra = self.numero_lote_insumo
        self.insumo.save()


class MedicamentoEntrada(BaseModel):
    unidade_saude = models.ForeignKey('saude.UnidadeSaude', verbose_name='Unidade de saúde', null=True, blank=True, on_delete=models.PROTECT)

    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, blank=True)
    quantidade_medicamento = models.IntegerField(blank=True)
    unidade_medicamento = models.CharField(max_length=7, choices=UNIDADE_CHOICES, blank=True)
    numero_lote_medicamento = models.CharField(max_length=50)
    data_vencimento_medicamento = models.DateField()

    def __str__(self):
        return self.medicamento.nome_medicamento

    @hook("after_create")
    def incrementar_quantidade_medicamento(self):
        self.medicamento.quantidade += int(self.quantidade_medicamento)
        self.medicamento.codigo_de_barra = self.numero_lote_medicamento
        self.medicamento.save()


class ProdutoEntrada(BaseModel):
    unidade_saude = models.ForeignKey('saude.UnidadeSaude', verbose_name='Unidade de saúde', null=True, blank=True, on_delete=models.PROTECT)

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, blank=True)
    quantidade_produto = models.IntegerField(blank=True)
    unidade_produto = models.CharField(max_length=7, choices=UNIDADE_CHOICES, blank=True)
    numero_lote_produto = models.CharField(max_length=50)
    data_vencimento_produto = models.DateField()

    def __str__(self):
        return self.produto.nome_produto
    
    @hook("after_create")
    def incrementar_quantidade_produto(self):
        self.produto.quantidade += int(self.quantidade_produto)
        self.produto.codigo_de_barra = self.numero_lote_produto
        self.produto.save()

class EntradaMaterialFarmacia(BaseModel):
    COMPRA, TRANSFERENCIA = range(2)
    TIPO_ENTRADA_CHOICES = [
        (COMPRA, 'COMPRA'),
        (TRANSFERENCIA, 'TRANSFERÊNCIA')
    ]

    unidade_saude = models.ForeignKey('saude.UnidadeSaude', verbose_name='Unidade de saúde', null=True, blank=True, on_delete=models.PROTECT)
    farmacia = models.ForeignKey(Farmacia, on_delete=models.PROTECT)

    data_entrada = models.DateField()
    numero_pedido = models.CharField('N° Pedido', unique=True, error_messages={'unique': 'Uma entrada com esse número de pedido já existe.'}, max_length=50)
    farmaceutico_responsavel = models.ForeignKey('saude_cadastro.Profissional', on_delete=models.PROTECT, blank=True, null=True)
    tipo_entrada = models.IntegerField(choices=TIPO_ENTRADA_CHOICES, default=COMPRA)
    fornecedor = models.CharField('Fornecedor', max_length=200)
    numero_nota_fiscal = models.CharField('N° Nota Fiscal', unique=True, error_messages={'unique': 'Uma entrada com esse número de nota fiscal já existe.'}, max_length=50)
    empenho = models.CharField('Empenho', max_length=200)
    processo = models.CharField('Processo', unique=True, error_messages={'unique': 'Uma entrada com esse processo já existe.'}, max_length=50)
    
    insumo_entrada = models.ManyToManyField(InsumoEntrada, blank=True)
    medicamento_entrada = models.ManyToManyField(MedicamentoEntrada, blank=True)
    produto_entrada = models.ManyToManyField(ProdutoEntrada, blank=True)

    # SOLICITADO, DEFERIDO, CONCLUIDO, REJEITADO = range(4)
    # TIPO_SITUACAO_CHOICES = [
    #     (SOLICITADO, 'SOLICITADO'),
    #     (DEFERIDO, 'DEFERIDO'),
    #     (CONCLUIDO, 'CONCLUÍDO'),
    #     (REJEITADO, 'REJEITADO'),
    # ]
    # situacao_requisicao = models.IntegerField(choices=TIPO_SITUACAO_CHOICES, default=SOLICITADO)

    def __str__(self):
        return f'{self.numero_pedido} - Data da entrada: {self.data_entrada} - Farmácia: {self.farmacia}'
