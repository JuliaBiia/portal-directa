from django.shortcuts import render
import datetime
from uuid import UUID
from dal import autocomplete
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from .models import SolicitacaoAlvaraFuncionamento
from .forms import SolicitacaoAlvaraFuncionamentoForm

class SemurbSolicitarAlvaraFuncionamentoView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = SolicitacaoAlvaraFuncionamento
    form_class = SolicitacaoAlvaraFuncionamentoForm
    template_name = 'portal_directa/semurb_solicitar_alvara_funcionamento.html'
    success_url = reverse_lazy('portal_directa:semurb_solicitar_alvara_funcionamento')
    success_message = "Solicitação de Alvará de Funcionamento enviada com sucesso!"

    def form_valid(self, form):
        form.instance.solicitante = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Solicitar Alvará de Funcionamento'
        return context