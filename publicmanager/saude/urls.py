from django.urls import path

from  .api import views as api_views
from .views import SalasListView, ManualListView

app_name = 'saude'

urlpatterns = [
    ## Lista de Salas
    path('listagem/', SalasListView.as_view(), name='selecao_salas_list'),
    path('manuais/', ManualListView.as_view(), name='manuis_list'),
    
    # Saúde API
    path('api/atualizar-sala/<uuid:pk>/', api_views.AtualizarUnidadeLoginAPIView.as_view(), name='api_atualizar_unidade_login_sala'),
]