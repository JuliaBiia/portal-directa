from django.urls import path
from publicmanager.saude_cadastro import views
from publicmanager.saude_cadastro.api import views as api_cadastro

app_name = 'saude_cadastro'

urlpatterns = [
    ## TipoClinica
    path('tipoclinica/', views.TipoClinicaListView.as_view(), name='tipoclinica_list'),
    path('tipoclinica/criar/', views.TipoClinicaCreateView.as_view(), name='tipoclinica_add'),
    path('tipoclinica/<uuid:pk>/atualizar/', views.TipoClinicaUpdateView.as_view(), name='tipoclinica_update'),
    path('tipoclinica/<uuid:pk>/deletar/', views.TipoClinicaDeleteView.as_view(), name='tipoclinica_delete'),
    ## Convênios
    path('convenios/', views.ConvenioListView.as_view(), name='convenio_list'),
    path('convenio/criar/', views.ConvenioCreateView.as_view(), name='convenio_add'),
    path('convenio/<uuid:pk>/atualizar/', views.ConvenioUpdateView.as_view(), name='convenio_update'),
    path('convenio/<uuid:pk>/deletar/', views.ConvenioDeleteView.as_view(), name='convenio_delete'),
    ## CID
    path('cids/', views.CIDListView.as_view(), name='cid_list'),
    path('cid/criar/', views.CIDCreateView.as_view(), name='cid_add'),
    path('cid/<uuid:pk>/atualizar/', views.CIDUpdateView.as_view(), name='cid_update'),
    path('cid/<uuid:pk>/deletar/', views.CIDDeleteView.as_view(), name='cid_delete'),
    ## Destino de óbito
    path('destino-obito/', views.DestinoObitoListView.as_view(), name='destinoobito_list'),
    path('destino-obito/criar/', views.DestinoObitoCreateView.as_view(), name='destinoobito_add'),
    path('destino-obito/<uuid:pk>/atualizar/', views.DestinoObitoUpdateView.as_view(), name='destinoobito_update'),
    path('destino-obito/<uuid:pk>/deletar/', views.DestinoObitoDeleteView.as_view(), name='destinoobito_delete'),
    ## Tipo de Exames
    path('tipo-exames/', views.TipoExameListView.as_view(), name='tipoexame_list'),
    path('tipo-exame/criar/', views.TipoExameCreateView.as_view(), name='tipoexame_add'),
    path('tipo-exame/<uuid:pk>/atualizar/', views.TipoExameUpdateView.as_view(), name='tipoexame_update'),
    path('tipo-exame/<uuid:pk>/deletar/', views.TipoExameDeleteView.as_view(), name='tipoexame_delete'),
    ## Exame
    path('exames/', views.ExameListView.as_view(), name='exame_list'),
    path('exame/criar/', views.ExameCreateView.as_view(), name='exame_add'),
    path('exame/<uuid:pk>/atualizar/', views.ExameUpdateView.as_view(), name='exame_update'),
    path('exame/<uuid:pk>/deletar/', views.ExameDeleteView.as_view(), name='exame_delete'),
    ## Tipo de Classificação de Risco
    path('tipo-classificacao-risco/', views.TipoClassificacaoRiscoListView.as_view(), name='tipoclassificacaorisco_list'),
    ## Tipo de História Clínica
    path('tipo-historia-clinica/', views.TipoHistoriaClinicaListView.as_view(), name='tipohistoriaclinica_list'),
    path('tipo-historia-clinica/criar/', views.TipoHistoriaClinicaCreateView.as_view(), name='tipohistoriaclinica_add'),
    path('tipo-historia-clinica/<uuid:pk>/atualizar/', views.TipoHistoriaClinicaUpdateView.as_view(), name='tipohistoriaclinica_update'),
    path('tipo-historia-clinica/<uuid:pk>/deletar/', views.TipoHistoriaClinicaDeleteView.as_view(), name='tipohistoriaclinica_delete'),
    ## Tipo de Posologia
    path('tipo-posologia/', views.TipoPosologiaListView.as_view(), name='tipoposologia_list'),
    path('tipo-posologia/criar/', views.TipoPosologiaCreateView.as_view(), name='tipoposologia_add'),
    path('tipo-posologia/<uuid:pk>/atualizar/', views.TipoPosologiaUpdateView.as_view(), name='tipoposologia_update'),
    path('tipo-posologia/<uuid:pk>/deletar/', views.TipoPosologiaDeleteView.as_view(), name='tipoposologia_delete'),
    ## Transporte
    path('transportes/', views.TransporteListView.as_view(), name='transporte_list'),
    path('transporte/criar/', views.TransporteCreateView.as_view(), name='transporte_add'),
    path('transporte/<uuid:pk>/atualizar/', views.TransporteUpdateView.as_view(), name='transporte_update'),
    path('transporte/<uuid:pk>/deletar/', views.TransporteDeleteView.as_view(), name='transporte_delete'),
    ## Sala
    path('salas/', views.SalaListView.as_view(), name='sala_list'),
    path('sala/criar/', views.SalaCreateView.as_view(), name='sala_add'),
    path('sala/<uuid:pk>/atualizar/', views.SalaUpdateView.as_view(), name='sala_update'),
    path('sala/<uuid:pk>/deletar/', views.SalaDeleteView.as_view(), name='sala_delete'),
    ## Profissional
    path('profissional/', views.ProfissionalListView.as_view(), name='profissional_list'),
    path('profissional/criar/', views.ProfissionalCreateView.as_view(), name='profissional_add'),
    path('profissional/<uuid:pk>/atualizar/', views.ProfissionalUpdateView.as_view(), name='profissional_update'),
    path('profissional/<uuid:pk>/deletar/', views.ProfissionalDeleteView.as_view(), name='profissional_delete'),

    ## Setor
    path('setores/', views.SetorListView.as_view(), name='setor_list'),
    path('setor/criar/', views.SetorCreateView.as_view(), name='setor_add'),
    path('setor/<uuid:pk>/atualizar/', views.SetorUpdateView.as_view(), name='setor_update'),
    path('setor/<uuid:pk>/deletar/', views.SetorDeleteView.as_view(), name='setor_delete'),

    ## Painel Chamado
    path('paineis/', views.PainelChamadaListView.as_view(), name='painel_chamada_list'),
    path('painel/criar/', views.PainelChamadaCreateView.as_view(), name='painel_chamada_add'),
    path('painel/<uuid:pk>/atualizar/', views.PainelChamadaUpdateView.as_view(), name='painel_chamada_update'),
    path('painel/<uuid:pk>/deletar/', views.PainelChamadaDeleteView.as_view(), name='painel_chamada_delete'),
    
    # API
    path('api/cids/', api_cadastro.CidAPIView.as_view(), name='api_cid_list'),
    path('api/cid-autocomplete/', api_cadastro.CidAPIAutocomplete.as_view(), name='api_cid_autocomplete'),
    path('api/exames/', api_cadastro.ExameAPIView.as_view(), name='api_exame_list'),
    path('api/procedimentos/', api_cadastro.ProcedimentoAPIView.as_view(), name='api_procedimento_list'),
    path('api/procedimentos-detail/<uuid:pk>/', api_cadastro.ProcedimentoDetailAPIView.as_view(), name='api_procedimento_detail'),

    path('api/tipo-classificacao-risco/<uuid:pk>/atualizar/', api_cadastro.TipoClassificacaoRiscoUpdateAPIView.as_view(), name='api_tipo_classificacao_risco_update'),
    path('api/profissionais/', api_cadastro.ProfissionalAPIView.as_view(), name='api_profissional_view'),
    path('api/profissionais/recepcaonoturna/<uuid:pk>/atualizar/', api_cadastro.ProfissionalRecepcaoNoturnoAPIView.as_view(), name='api_profissional_recepcaonoturno_view'),
]


