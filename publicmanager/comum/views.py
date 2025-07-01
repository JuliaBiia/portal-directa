from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseServerError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from .forms import BancoForm, EstadoCivilForm, MunicipioForm, GrupoDeficienciaForm, DeficienciaForm, RacaForm
from .models import Banco, EstadoCivil, Municipio, GrupoDeficiencia, Deficiencia, Raca
class BancoListView(LoginRequiredMixin, ListView):
    model = Banco
    context_object_name = 'bancos'
    template_name = '/comum/banco.html'

class BancoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Banco
    template_name = 'comum/banco_create_update_form.html'
    form_class = BancoForm
    success_url = '/banco/'
    success_message = 'Seus dados foram cadastrado conforme preencimento do formulário.'


class BancoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Banco
    template_name = 'comum/banco_create_update_form.html'
    form_class = BancoForm
    success_url = '/comum/banco/'
    success_message = 'Seus dados foram atualizados conforme preencimento do formulário.'


class BancoDeleteView(LoginRequiredMixin, DeleteView):
    model = Banco
    template_name = "banco.html"
    success_url = '/comum/banco/'
    success_message = 'Seus dados foram deletados conforme solicitado.'


class EstadoCivilListView(LoginRequiredMixin, ListView):
    model = EstadoCivil
    context_object_name = 'estadoscivis'
    template_name = 'comum/estadocivil.html'


class EstadoCivilCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = EstadoCivil
    template_name = 'comum/estadocivil_create_update_form.html'
    form_class = EstadoCivilForm
    success_url = '/comum/estadocivil/'
    success_message = 'Seus dados foram cadastrado conforme preencimento do formulário.'


class EstadoCivilUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = EstadoCivil
    template_name = 'comum/estadocivil_create_update_form.html'
    form_class = EstadoCivilForm
    success_url = '/comum/estadocivil/'
    success_message = 'Seus dados foram atualizados conforme preencimento do formulário.'


class EstadoCivilDeleteView(LoginRequiredMixin, DeleteView):
    model = EstadoCivil
    template_name = "estadocivil.html"
    success_url = '/comum/estadocivil/'
    success_message = 'Seus dados foram deletados conforme solicitado.'


class MunicipioListView(LoginRequiredMixin, ListView):
    model = Municipio
    context_object_name = 'municipios'
    template_name = 'comum/municipio.html'


class MunicipioCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Municipio
    template_name = 'comum/municipio_create_update_form.html'
    form_class = MunicipioForm
    success_url = '/comum/municipio/'
    success_message = 'Seus dados foram cadastrado conforme preencimento do formulário.'


class MunicipioUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Municipio
    template_name = 'comum/municipio_create_update_form.html'
    form_class = MunicipioForm
    success_url = '/comum/municipio/'
    success_message = 'Seus dados foram atualizados conforme preencimento do formulário.'


class GrupoDeficienciaListView(LoginRequiredMixin, ListView):
    model = GrupoDeficiencia
    context_object_name = 'gruposdeficiencia'
    template_name = 'comum/grupodeficiencia.html'


class GrupoDeficienciaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = GrupoDeficiencia
    template_name = 'comum/grupodeficiencia_create_update_form.html'
    form_class = GrupoDeficienciaForm
    success_url = '/comum/grupodeficiencia/'
    success_message = 'Seus dados foram cadastrado conforme preencimento do formulário.'


class GrupoDeficienciaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = GrupoDeficiencia
    template_name = 'comum/grupodeficiencia_create_update_form.html'
    form_class = GrupoDeficienciaForm
    success_url = '/comum/grupodeficiencia/'
    success_message = 'Seus dados foram atualizados conforme preencimento do formulário.'


class GrupoDeficienciaDeleteView(LoginRequiredMixin, DeleteView):
    model = GrupoDeficiencia
    template_name = "grupodeficiencia.html"
    success_url = '/comum/grupodeficiencia/'
    success_message = 'Seus dados foram deletados conforme solicitado.'

    def post(self, request, *args, **kwargs):
        deficiencia = Deficiencia.objects.filter(grupo_deficiencia__id=self.kwargs["pk"])
        if deficiencia:
            messages.success(request, (
                'O grupo de deficiência não pode ser excluído pois está vinculado a tipos de deficiência.'))
            return redirect('grupodeficiencia_list')
        else:
            return self.delete(request, *args, **kwargs)


class DeficienciaListView(LoginRequiredMixin, ListView):
    model = Deficiencia
    context_object_name = 'deficiencias'
    template_name = 'comum/deficiencia.html'


class DeficienciaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Deficiencia
    template_name = 'comum/deficiencia_create_update_form.html'
    form_class = DeficienciaForm
    success_url = '/comum/deficiencia/'
    success_message = 'Seus dados foram cadastrado conforme preencimento do formulário.'


class DeficienciaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Deficiencia
    template_name = 'comum/deficiencia_create_update_form.html'
    form_class = DeficienciaForm
    success_url = '/comum/deficiencia/'
    success_message = 'Seus dados foram atualizados conforme preencimento do formulário.'


class DeficienciaDeleteView(LoginRequiredMixin, DeleteView):
    model = Deficiencia
    template_name = "deficiencia.html"
    success_url = '/comum/deficiencia/'
    success_message = 'Seus dados foram deletados conforme solicitado.'

class RacaListView(LoginRequiredMixin, ListView):
    model = Raca
    context_object_name = 'racas'
    template_name = 'comum/raca.html'


class RacaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Raca
    template_name = 'comum/raca_create_update_form.html'
    form_class = RacaForm
    success_url = '/comum/raca/'
    success_message = 'Seus dados foram cadastrado conforme preencimento do formulário.'


class RacaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Raca
    template_name = 'comum/raca_create_update_form.html'
    form_class = RacaForm
    success_url = '/comum/raca/'
    success_message = 'Seus dados foram atualizados conforme preencimento do formulário.'


class RacaDeleteView(LoginRequiredMixin, DeleteView):
    model = Raca
    template_name = "raca.html"
    success_url = '/comum/raca/'
    success_message = 'Seus dados foram deletados conforme solicitado.'