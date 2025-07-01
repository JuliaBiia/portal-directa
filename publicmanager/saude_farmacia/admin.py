from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from publicmanager.saude_farmacia.models import (
    InsumoEntrada, Medicamento, Insumo, Farmacia, InsumoRequisitado, MedicamentoEntrada, 
    MedicamentoRequisitado, Produto, ProdutoEntrada, ProdutoRequisitado, RequisicaoMaterialFarmacia, EntradaMaterialFarmacia,
    PrincipioAtivo
)


@admin.register(Farmacia)
class FarmaciaAdmin(SimpleHistoryAdmin):
    list_display= ('nome_farmacia', 'unidade_saude')
    readonly_fields = ['unidade_saude']


@admin.register(PrincipioAtivo)
class PrincipioAtivoAdmin(admin.ModelAdmin):
    list_display= ('nome',)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display= ('nome_produto', 'codigo_de_barra', 'tipo_produto', 'quantidade')
    readonly_fields = ['unidade_saude']

@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    search_fields= ('nome_medicamento', )
    list_display= ('nome_medicamento', 'codigo_de_barra', 'tipo_medicamento', 'quantidade')
    # readonly_fields = ['unidade_saude', 'principio_ativo_medicamento']
    # autocomplete_fields = ['unidade_saude', 'principio_ativo_medicamento']

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display= ('nome_insumo', 'codigo_de_barra', 'quantidade')
    readonly_fields = ['unidade_saude']


@admin.register(InsumoRequisitado)
class InsumoRequisitadoAdmin(admin.ModelAdmin):
    list_display= ('insumo', 'quantidade_insumo', 'unidade_insumo')
    readonly_fields = ['unidade_saude']

@admin.register(MedicamentoRequisitado)
class MedicamentoRequisitadoAdmin(admin.ModelAdmin):
    list_display= ('medicamento', 'quantidade_medicamento', 'unidade_medicamento')
    readonly_fields = ['unidade_saude']

@admin.register(ProdutoRequisitado)
class ProdutoRequisitadoAdmin(admin.ModelAdmin):
    list_display= ('produto', 'quantidade_produto', 'unidade_produto')
    readonly_fields = ['unidade_saude']

@admin.register(RequisicaoMaterialFarmacia)
class RequisicaoMaterialFarmaciaAdmin(admin.ModelAdmin):
    list_display= ('numero_pedido', 'data_solicitacao', 'farmaceutico_solicitante', 'farmacia')
    readonly_fields = ['unidade_saude', 'farmaceutico_solicitante', 'farmacia', 'insumo_requisitado', 'medicamento_requisitado', 'produto_requisitado']


@admin.register(InsumoEntrada)
class InsumoEntradaAdmin(admin.ModelAdmin):
    list_display= ('insumo', 'quantidade_insumo', 'unidade_insumo', 'numero_lote_insumo', 'data_vencimento_insumo')
    readonly_fields = ['unidade_saude']

@admin.register(MedicamentoEntrada)
class MedicamentoEntradaAdmin(admin.ModelAdmin):
    list_display= ('medicamento', 'quantidade_medicamento', 'unidade_medicamento', 'numero_lote_medicamento', 'data_vencimento_medicamento')
    readonly_fields = ['unidade_saude']

@admin.register(ProdutoEntrada)
class ProdutoEntradaAdmin(admin.ModelAdmin):
    list_display= ('produto', 'quantidade_produto', 'unidade_produto', 'numero_lote_produto', 'data_vencimento_produto')
    readonly_fields = ['unidade_saude']

@admin.register(EntradaMaterialFarmacia)
class EntradaMaterialFarmaciaAdmin(admin.ModelAdmin):
    list_display= ('data_entrada', 'numero_pedido', 'farmaceutico_responsavel')
    readonly_fields = ['unidade_saude', 'farmacia', 'farmaceutico_responsavel', 'insumo_entrada', 'produto_entrada', 'medicamento_entrada']
    # autocomplete_fields=('insumo_entrada',)
    # search_fields= ('numero_pedido', 'insumo_entrada', )