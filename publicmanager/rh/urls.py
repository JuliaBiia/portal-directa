from django.urls import path
from publicmanager.rh import views

app_name = 'rh'

urlpatterns = [
    ## Cargo
    path('cargo/', views.CargoEmpregoListView.as_view(), name='cargo_list'),
    path('cargo/add/', views.CargoEmpregoCreateView.as_view(), name='cargo_add'),
    path('cargo/update/<pk>', views.CargoEmpregoUpdateView.as_view(), name='cargo_update'),
    path('cargo/delete/<pk>', views.CargoEmpregoDeleteView.as_view(), name='cargo_delete'),
    ## Função
    path('funcao/', views.FuncaoListView.as_view(), name='funcao_list'),
    path('funcao/add/', views.FuncaoCreateView.as_view(), name='funcao_add'),
    path('funcao/update/<pk>', views.FuncaoUpdateView.as_view(), name='funcao_update'),
    path('funcao/delete/<pk>', views.FuncaoDeleteView.as_view(), name='funcao_delete'),
    ## Jornada de Trabalho
    path('jornada_trabalho/', views.JornadaTrabalhoListView.as_view(), name='jornada_trabalho_list'),
    path('jornada_trabalho/add/', views.JornadaTrabalhoCreateView.as_view(), name='jornada_trabalho_add'),
    path('jornada_trabalho/update/<pk>', views.JornadaTrabalhoUpdateView.as_view(), name='jornada_trabalho_update'),
    path('jornada_trabalho/delete/<pk>', views.JornadaTrabalhoDeleteView.as_view(), name='jornada_trabalho_delete'),
    ## Jornada de Trabalho
    path('regime_juridico/', views.RegimeJuridicoListView.as_view(), name='regime_juridico_list'),
    path('regime_juridico/add/', views.RegimeJuridicoCreateView.as_view(), name='regime_juridico_add'),
    path('regime_juridico/update/<pk>', views.RegimeJuridicoUpdateView.as_view(), name='regime_juridico_update'),
    path('regime_juridico/delete/<pk>', views.RegimeJuridicoDeleteView.as_view(), name='regime_juridico_delete'),
    ## Pessoa Física
    path('pessoafisica/', views.PessoaFisicaListView.as_view(), name='pessoafisica_list'),
    path('pessoa/add/', views.PessoaFisicaCreateView.as_view(), name='pessoafisica_add'),
    path('pessoafisica/update/<pk>', views.PessoaFisicaUpdateView.as_view(), name='pessoafisica_update'),
    path('pessoafisica/delete/<pk>', views.PessoaFisicaDeleteView.as_view(), name='pessoafisica_delete'),
    ## Pessoa Jurídica
    path('pessoajuridica/', views.PessoaJuridicaListView.as_view(), name='pessoajuridica_list'),
    path('pessoajuridica/add/', views.PessoaJuridicaCreateView.as_view(), name='pessoajuridica_add'),
    path('pessoajuridica/update/<pk>', views.PessoaJuridicaUpdateView.as_view(), name='pessoajuridica_update'),
    path('pessoajuridica/delete/<pk>', views.PessoaJuridicaDeleteView.as_view(), name='pessoajuridica_delete'),
    ## Nível de Escolaridade
    path('nivel_escolaridade/', views.NivelEscolaridadeListView.as_view(), name='nivel_escolaridade_list'),
    path('nivel_escolaridade/add/', views.NivelEscolaridadeCreateView.as_view(), name='nivel_escolaridade_add'),
    path('nivel_escolaridade/update/<pk>', views.NivelEscolaridadeUpdateView.as_view(), name='nivel_escolaridade_update'),
    path('nivel_escolaridade/delete/<pk>', views.NivelEscolaridadeDeleteView.as_view(), name='nivel_escolaridade_delete'),
    ## Situação
    path('situacao/', views.SituacaoListView.as_view(), name='situacao_list'),
    path('situacao/add/', views.SituacaoCreateView.as_view(), name='situacao_add'),
    path('situacao/update/<pk>', views.SituacaoUpdateView.as_view(), name='situacao_update'),
    path('situacao/delete/<pk>', views.SituacaoDeleteView.as_view(), name='situacao_delete'),
    ## Servidor
    path('servidor/', views.ServidorListView.as_view(), name='servidor_list'),
    path('servidor/add/', views.ServidorCreateView.as_view(), name='servidor_add'),
    path('servidor/update/<pk>', views.ServidorUpdateView.as_view(), name='servidor_update'),
]
