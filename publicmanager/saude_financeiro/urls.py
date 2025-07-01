from django.urls import path
from publicmanager.saude_financeiro import views

app_name = 'saude_financeiro'

urlpatterns = [
    path('relatorio-procedimentos/gerar/', views.RelatorioProcedimentosTemplateView.as_view(), name='procedimentos_gerar_view'),
    path('relatorio-consolidado-detalhado/pdf/', views.RelatorioConsolidadoDetalhadoPDFView.as_view(), name='relatorio_consolidado_detalhado_pdf'),
    path('relatorio-consolidado-resumido/pdf/', views.RelatorioConsolidadoResumidoPDFView.as_view(), name='relatorio_consolidado_resumido_pdf'),
    path('Boletim/producao/individualizados/', views.BoletimProducaoIndividualizados.as_view(), name='boletimproducao_dados_individualizados'),
]
