from django.urls import path, include
from .api import views as api_enfermagem
from rest_framework.routers import DefaultRouter

from publicmanager.saude_enfermagem import views
from publicmanager.saude_enfermagem.api import views as api_enfermagem

enfermagem_atendimento_router = DefaultRouter()
enfermagem_atendimento_router.register('atendimento', api_enfermagem.SolicitacoesAtendimentoViewSet, basename='atendimentos')

enfermagem_admin_procedimento_router = DefaultRouter()
enfermagem_admin_procedimento_router.register('admin-procedimento', api_enfermagem.SolicitacoesAdministracaoProcedimentoViewSet, basename='admin-procedimento')

app_name = 'saude_enfermagem'

urlpatterns = [
    ## Exames Laboratóriais
    path('exames-laboratoriais/listagem/', views.ExamesLaboratoriaisListView.as_view(), name='exames_laboratoriais_list'),
    path('exames-laboratoriais/<uuid:pk>/atualizar/', views.ExamesLaboratoriaisChamadoUpdateView.as_view(), name='exames_laboratoriais_update'),
    path('exames-laboratoriais/<uuid:pk>/detalhes/', views.ExamesLaboratoriaisDetailView.as_view(), name='exames_laboratoriais_detalhes'),

    ## Exames Imagem
    path('exames-imagem/listagem/', views.ExamesImagemListView.as_view(), name='exames_imagem_list'),
    path('exames-imagem/<uuid:pk>/atualizar/', views.ExamesImagemChamadoUpdateView.as_view(), name='exames_imagem_update'),
    path('exames-imagem/<uuid:pk>/detalhes/', views.ExamesImagemDetailView.as_view(), name='exames_imagem_detalhes'),

    ## Medicações
    path('medicacao/listagem/', views.AdministacaoMedicacaoListView.as_view(), name='administracao_medicacao_list'),
    path('medicacoes/<uuid:pk>/atualizar/', views.AdministacaoMedicacaoChamadoUpdateView.as_view(), name='administracao_medicacao_update'),
    path('medicacao/<uuid:pk>/detalhes/', views.AdministracaoMedicacaoDetailView.as_view(), name='administracao_medicacao_detalhes'),

    ## Administração Medicação Vacina
    path('medicamento-vacina/espera/listagem/', views.AdministracaoMedicamentoVacinaEmAbertoListView.as_view(), name='administracao_medicamento_vacina_aberto_list'),
    path('medicamento-vacina/', views.AdministracaoMedicacaoVacinaCreateView.as_view(), name='administracao_medicacao_vacina_create'),
    path('medicamento-vacina/<uuid:pk>/atualizar/', views.AdministracaoMedicamentoVacinaUpdateView.as_view(), name='administracao_medicacao_vacina_update'),
    path('medicamento-vacina/<uuid:pk>/detalhes/', views.AdministracaoMedicamentoVacinaDetailView.as_view(), name='administracao_medicacao_vacina_detail'),

    ## Procedimentos
    path('procedimentos/listagem/', views.ProcedimentosListView.as_view(), name='procedimentos_list'),
    path('procedimentos/<uuid:pk>/atualizar/', views.ProcedimentosChamadoUpdateView.as_view(), name='procedimentos_update'),
    path('procedimentos/<uuid:pk>/detalhes/', views.ProcedimentosDetailView.as_view(), name='procedimentos_detail'),

    ## Administração Procedimentos Eletivo
    path('procedimentos/listagem/madministracao-procedimentos/', views.AdministracaoProcedimentosListView.as_view(), name='administracao_procedimentos_list'),
    path('procedimentos/update/<uuid:pk>/atualizar/', views.AdministracaoProcedimentoUpdateView.as_view(), name='administracao_procedimento_update'),
    path('procedimentos/atendimento/<uuid:pk>/criar/', views.AdministracaoProcedimentoCreateView.as_view(), name='administracao_procedimento_create'),
    path('administracao-procedimentos/<uuid:pk>/detalhes/', views.AdministracaoProcedimentoDetailView.as_view(), name='administracao_procedimento_detail'),

    ## Listegem de Atendimentos
    path('atendimentos/realizados/listagem/', views.AtendimentosRealizadosListView.as_view(), name='atendimentos_realizados_list'),

    ## Relatórios
    path('atendimentos-realizados-pdf/', views.AtendimentosRealizadosPDFView.as_view(), name='atendimento_realizados_pdf_view'),

    # API
    path('api/atualizar-chamado/<uuid:pk>/', api_enfermagem.ChamadoEnfermagemUpdateAPIView.as_view(), name='api_atualizar_chamado'),
    path('api/criar/receita/', api_enfermagem.ReceitaMedicamentoCreateAPIView.as_view(), name='api_receita_medicamento_create'),
    path('api/receita-medicacao/detalhes/', api_enfermagem.ReceitaMedicamentoAPIView.as_view(), name='api_receita_medicamento_view'),
    path('api/administracao-medicacao-vacina/listagem/', api_enfermagem.SituacaoAdministracaoMedicamentoAPIView.as_view(), name='api_situacao_administracao_medicamento_view'),
    path('api/administracao-medicacao-vacina/<uuid:pk>/finalizar/', api_enfermagem.FinalizarSituacaoAdministracaoMedicamentoVacinaAPIView.as_view(), name='api_finalizar_situacao_administracao_medicamento_vacina_view'),
    path('api/', include(enfermagem_atendimento_router.urls)),
    path('api/procedimentos/', include(enfermagem_admin_procedimento_router.urls)),

    #API (procedimento)
    path('api/criar/receita-procedimento/', api_enfermagem.ReceitaProcedimentoCreateAPIView.as_view(), name='api_receita_procedimento_create'),

]