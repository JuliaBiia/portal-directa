from django.urls import path, include
from rest_framework.routers import DefaultRouter
from publicmanager.portal_directa import views

app_name = 'portal_directa'

urlpatterns = [
    path('pacientes/semurb/solicitar-alvara-funcionamento', views.SemurbSolicitarAlvaraFuncionamentoView.as_view(), name='semurb_solicitar_alvara_funcionamento'),

    # path('novaPagina/', views.novaPagina, name='nova_pagina')
]