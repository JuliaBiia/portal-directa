from django.urls import path
from django.contrib.auth.views import LogoutView

from .api import views as api_autenticacao
from publicmanager.autenticacao import views as autenticacao

app_name = 'autenticacao'

urlpatterns = [
    path('', autenticacao.saude_login_view, name='login'),
    path('esqueceu/senha/', autenticacao.AlterarSenhaCreateView.as_view(), name='esqueceu_senha'),
    path('alterar-senha/', autenticacao.AlterarSenhaView.as_view(), name='alterar_senha'),
    path('sair/', LogoutView.as_view(next_page='/'), name='sair'),

    # API
    path('unidades/', api_autenticacao.UnidadesPorCpfAPIView.as_view(), name='get_unidades_por_cpf'),
]

