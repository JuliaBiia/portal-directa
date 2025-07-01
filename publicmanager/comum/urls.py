from django.urls import path
from publicmanager.comum import views

app_name = 'comum'

urlpatterns = [
    ## Banco
    path('banco/', views.BancoListView.as_view(), name='banco_list'),
    path('banco/add/', views.BancoCreateView.as_view(), name='banco_add'),
    path('banco/update/<pk>', views.BancoUpdateView.as_view(), name='banco_update'),
    path('banco/delete/<pk>', views.BancoDeleteView.as_view(), name='banco_delete'),
    
    ## EstadoCivil
    path('estadocivil/', views.EstadoCivilListView.as_view(), name='estadocivil_list'),
    path('estadocivil/add/', views.EstadoCivilCreateView.as_view(), name='estadocivil_add'),
    path('estadocivil/update/<pk>', views.EstadoCivilUpdateView.as_view(), name='estadocivil_update'),
    path('estadocivil/delete/<pk>', views.EstadoCivilDeleteView.as_view(), name='estadocivil_delete'),
    
    ## Municipio
    path('municipio/', views.MunicipioListView.as_view(), name='municipio_list'),
    path('municipio/add/', views.MunicipioCreateView.as_view(), name='municipio_add'),
    path('municipio/update/<pk>', views.MunicipioUpdateView.as_view(), name='municipio_update'),
    
    ## GrupoDeficiencia
    path('grupodeficiencia/', views.GrupoDeficienciaListView.as_view(), name='grupodeficiencia_list'),
    path('grupodeficiencia/add/', views.GrupoDeficienciaCreateView.as_view(), name='grupodeficiencia_add'),
    path('grupodeficiencia/update/<pk>', views.GrupoDeficienciaUpdateView.as_view(), name='grupodeficiencia_update'),
    path('grupodeficiencia/delete/<pk>', views.GrupoDeficienciaDeleteView.as_view(), name='grupodeficiencia_delete'),
    
    ## Deficiencia
    path('deficiencia/', views.DeficienciaListView.as_view(), name='deficiencia_list'),
    path('deficiencia/add/', views.DeficienciaCreateView.as_view(), name='deficiencia_add'),
    path('deficiencia/update/<pk>', views.DeficienciaUpdateView.as_view(), name='deficiencia_update'),
    path('deficiencia/delete/<pk>', views.DeficienciaDeleteView.as_view(), name='deficiencia_delete'),
    
    ## Raca
    path('raca/', views.RacaListView.as_view(), name='raca_list'),
    path('raca/add/', views.RacaCreateView.as_view(), name='raca_add'),
    path('raca/update/<pk>', views.RacaUpdateView.as_view(), name='raca_update'),
    path('raca/delete/<pk>', views.RacaDeleteView.as_view(), name='raca_delete'),
]
