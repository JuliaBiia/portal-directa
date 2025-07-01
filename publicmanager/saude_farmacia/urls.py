from django.urls import path

from .api import views as api_views
from publicmanager.saude_farmacia import views

app_name = 'saude_farmacia'

urlpatterns = [
    ## Princípio Ativo
    path('principioativo/', views.PrincipioAtivoListView.as_view(), name='principioativo_list'),
    path('principioativo/criar/', views.PrincipioAtivoCreateView.as_view(), name='principioativo_add'),
    path('principioativo/<uuid:pk>/atualizar/', views.PrincipioAtivoUpdateView.as_view(), name='principioativo_update'),
    path('principioativo/<uuid:pk>/deletar/', views.PrincipioAtivoDeleteView.as_view(), name='principioativo_delete'),
    ## Farmácia
    path('farmacias/', views.FarmaciaListView.as_view(), name='farmacia_list'),
    path('farmacia/criar/', views.FarmaciaCreateView.as_view(), name='farmacia_add'),
    path('farmacia/<uuid:pk>/atualizar/', views.FarmaciaUpdateView.as_view(), name='farmacia_update'),
    path('farmacia/<uuid:pk>/deletar/', views.FarmaciaDeleteView.as_view(), name='farmacia_delete'),
    ## Produto
    path('produtos/', views.ProdutoListView.as_view(), name='produto_list'),
    path('produto/criar/', views.ProdutoCreateView.as_view(), name='produto_add'),
    path('produto/<uuid:pk>/atualizar/', views.ProdutoUpdateView.as_view(), name='produto_update'),
    path('produto/<uuid:pk>/deletar/', views.ProdutoDeleteView.as_view(), name='produto_delete'),
    ## Medicamento
    path('medicamentos/', views.MedicamentoListView.as_view(), name='medicamento_list'),
    path('medicamento/criar/', views.MedicamentoCreateView.as_view(), name='medicamento_add'),
    path('medicamento/<uuid:pk>/atualizar/', views.MedicamentoUpdateView.as_view(), name='medicamento_update'),
    path('medicamento/<uuid:pk>/deletar/', views.MedicamentoDeleteView.as_view(), name='medicamento_delete'),
    ## Insumo Requisitado
    path('insumos/', views.InsumoListView.as_view(), name='insumo_list'),
    path('insumo/criar/', views.InsumoCreateView.as_view(), name='insumo_add'),
    path('insumo/<uuid:pk>/atualizar/', views.InsumoUpdateView.as_view(), name='insumo_update'),
    path('insumo/<uuid:pk>/deletar/', views.InsumoDeleteView.as_view(), name='insumo_delete'),
    ## Requisição de material da farmácia
    path('requisicoes-materiais-farmacia/', views.RequisicaoMaterialFarmaciaListView.as_view(), name='requisicao_material_farmacia_list'),
    path('requisicao-material-farmacia/criar/', views.RequisicaoMaterialFarmaciaCreateView.as_view(), name='requisicao_material_farmacia_add'),
    path('requisicao-material-farmacia/<uuid:pk>/atualizar/', views.RequisicaoMaterialFarmaciaUpdateView.as_view(), name='requisicao_material_farmacia_update'),
    path('requisicao-material-farmacia/<uuid:pk>/deletar/', views.RequisicaoMaterialFarmaciaDeleteView.as_view(), name='requisicao_material_farmacia_delete'),
    ## Entrada de material da farmácia
    path('entradas-materiais-farmacia/', views.EntradaMaterialFarmaciaListView.as_view(), name='entrada_material_farmacia_list'),
    path('entrada-material-farmacia/criar/', views.EntradaMaterialFarmaciaCreateView.as_view(), name='entrada_material_farmacia_add'),
    path('entrada-material-farmacia/<uuid:pk>/atualizar/', views.EntradaMaterialFarmaciaUpdateView.as_view(), name='entrada_material_farmacia_update'),
    path('entrada-material-farmacia/<uuid:pk>/deletar/', views.EntradaMaterialFarmaciaDeleteView.as_view(), name='entrada_material_farmacia_delete'),
    ## Controle de estoque de medicamento
    path('controle-estoque-medicamentos/', views.ControleEstoqueMedicamentoListView.as_view(), name='controle_estoque_medicamento_list'),
   
    ## Princípio Ativo
    path('principioativo/', views.PrincipioAtivoListView.as_view(), name='principioativo_list'),
    path('principioativo/criar/', views.PrincipioAtivoCreateView.as_view(), name='principioativo_add'),
    path('principioativo/<uuid:pk>/atualizar/', views.PrincipioAtivoUpdateView.as_view(), name='principioativo_update'),
    path('principioativo/<uuid:pk>/deletar/', views.PrincipioAtivoDeleteView.as_view(), name='principioativo_delete'),
    
    ## API
    path('api/lista/medicamentos/', api_views.MedicacoesAPIView.as_view(), name='api_lista_medicamentos'),
    path('api/lista/principio-ativo/', api_views.PrincipioAtivoAPIView.as_view(), name='api_principio_ativo'),
    path('api/produtomedico/detalhe/', api_views.ProdutoMedicoDetalheAPIView.as_view(), name='produtomedico_detalhe'),
    path('api/medicamento/detalhe/', api_views.MedicamentoDetalheAPIView.as_view(), name='medicamento_detalhe'),
    path('api/insumo/detalhe/', api_views.InsumoDetalheAPIView.as_view(), name='insumo_detalhe'),
    path('medicamento-autocomplete/', views.MedicamentoAutocomplete.as_view(), name='medicamento_autocomplete'),
]