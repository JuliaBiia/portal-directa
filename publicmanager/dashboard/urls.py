from django.urls import path
from publicmanager.dashboard import views
from .api import views as api_dashboard

app_name = 'dashboard'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('govbr', views.IndexxView.as_view(), name='index-govbr'),
    path('saude/redirecionamento/', views.saude_redirect_dashboard, name='saude_redirect_dashboard'),
    path('perfil/<uuid:pk>/detalhes/', views.MeuPerfilUpdate.as_view(), name="meu_perfil_atualizar"),

    # Saúde Painel Chamado
    path('<slug:slug2>/<slug:slug1>/', views.SaudePainelChamadaDetailView.as_view(), name='painel_chamado'),

    # Saúde API
    path('atendimento/painel/<uuid:pk>/listagem/', api_dashboard.SaudePainelChamadaDetailAPIView.as_view(), name='saude_painel_chamada_listagem'),

]
