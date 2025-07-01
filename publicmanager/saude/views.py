from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from publicmanager.saude.models import Manual
from publicmanager.saude.models import UnidadeLogin
from publicmanager.comum.utils import CheckUserTypeMixin
from publicmanager.saude_cadastro.models import Sala, UnidadeSetor

class SalasListView(LoginRequiredMixin, CheckUserTypeMixin, ListView):
    model = Sala
    template_name = "saude/salas_unidade_login.html"

    def get_queryset(self):
        setor = None
        if self.request.user.tipo_usuario == 'desenvolvedor' or self.request.user.tipo_usuario == 'administrador':
            setor = [UnidadeSetor.URGENCIA, UnidadeSetor.CONSULTORIO, UnidadeSetor.ENFERMARIA, UnidadeSetor.LABORATORIO, UnidadeSetor.RADIOLOGIA, UnidadeSetor.CLASSIFICACAO_RISCO]
        elif self.request.user.tipo_usuario == 'medico':
            setor = [UnidadeSetor.URGENCIA, UnidadeSetor.CONSULTORIO, UnidadeSetor.CLASSIFICACAO_RISCO]
        elif self.request.user.tipo_usuario == 'enfermeiro' or self.request.user.tipo_usuario == 'tecnico_enfermagem':
            setor = [UnidadeSetor.ENFERMARIA, UnidadeSetor.LABORATORIO, UnidadeSetor.CLASSIFICACAO_RISCO]
        elif self.request.user.tipo_usuario == 'radiologista':
            setor = [UnidadeSetor.RADIOLOGIA]
        
        queryset = super().get_queryset().filter(
            unidade_setor__unidade_saude=self.request.user.get_unidade_login().unidade,
            unidade_setor__tipo__in=setor
        )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['unidades_login'] = UnidadeLogin.objects.filter(unidade=self.request.user.get_unidade_login().unidade)
        context['inicial'] = self.request.GET.get('inicial')
        context['tipo_usuario'] = self.request.user.tipo_usuario
        context['setor'] = self.request.GET.get('setor')
        context['menu'] = self.request.GET.get('menu')
        return context
class ManualListView(LoginRequiredMixin, CheckUserTypeMixin, ListView):
    model = Manual
    context_object_name = 'pacientes'
    template_name = 'saude/manuais_list.html'

    def dispatch(self, request, *args, **kwargs):

        if self.request.user.tipo_usuario == None:
            messages.warning(self.request, 'Por favor, forneça uma URL válida.')
            return redirect(reverse('dashboard:index'))
        
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset().order_by('created_at')

        if self.request.user.tipo_usuario == "recepcionista":
            queryset = queryset.filter(tipo=Manual.RECEPCIONISTA)
            
        elif self.request.user.tipo_usuario == "medico":
            queryset = queryset.filter(tipo=Manual.MEDICO)

        elif self.request.user.tipo_usuario == "enfermeiro":
            queryset = queryset.filter(tipo=Manual.ENFERMEIRO)

        elif self.request.user.tipo_usuario == "radiologista":
            queryset = queryset.filter(tipo=Manual.RADIOLOGISTA)

        elif self.request.user.tipo_usuario == "farmaceutico":
            queryset = queryset.filter(tipo=Manual.FARMACEUTICO)

        elif self.request.user.tipo_usuario == "terapeuta":
            queryset = queryset.filter(tipo=Manual.TERAPEUTA)

        elif self.request.user.tipo_usuario == "nutricionista":
            queryset = queryset.filter(tipo=Manual.NUTRICIONISTA)
        
        # elif self.request.user.tipo_usuario == "administrador":
        #     queryset = queryset.filter(tipo=Manual.ADMINISTRADO)

        elif self.request.user.tipo_usuario == "suporte":
            queryset = queryset.filter(tipo=Manual.SUPORTE)
      
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['crumbs'] = [
            {'label': 'Manuais', 'url': '#'},
        ]

        return context