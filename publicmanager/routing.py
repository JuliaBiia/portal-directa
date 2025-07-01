from django.urls import path
from publicmanager.dashboard.consumers import PainelChamadaConsumer, AtualizarListagensConsumer

websocket_urlpatterns = [
    # Painel Chamado
    path('saude/painel/<slug:slug1>/<slug:slug2>/', PainelChamadaConsumer.as_asgi()),
    path('atualizar/listagem/<slug:slug1>/', AtualizarListagensConsumer.as_asgi()),
]
