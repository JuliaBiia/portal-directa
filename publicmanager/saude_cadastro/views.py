from uuid import UUID

from django.conf import settings
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.db.models.deletion import ProtectedError
from django.http.response import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from publicmanager.saude.models import UnidadeSaude
from publicmanager.autenticacao.models import Usuario
from publicmanager.comum.utils import CheckUserTypeMixin
from publicmanager.dashboard.utils import SaudeCheckHasPermission

from .models import (
    CID, Convenio, DestinoObito, Exame, Sala, TipoClassificacaoRisco, TipoClinica, TipoExame, 
    TipoHistoriaClinica, TipoPosologia, Transporte, Profissional, UnidadeSetor, PainelChamada
)
from .forms import (
    CIDForm, ConvenioForm, DestinoObitoForm, ExameForm, ProfissionalForm, ProfissionalUpdateViewForm, SalaForm, TipoClinicaForm,
    TipoExameForm, TipoHistoriaClinicaForm, TipoPosologiaForm, TransporteForm, SetorForm, PainelChamadaForm
)
class TipoClinicaListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = TipoClinica
    context_object_name = 'tipoclinicas'
    template_name = 'saude_cadastro/tipoclinica.html'

class TipoClinicaCreateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, CreateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = TipoClinica
    template_name = 'saude_cadastro/tipoclinica_create_update_form.html'
    form_class = TipoClinicaForm
    success_url = reverse_lazy('saude_cadastro:tipoclinica_list')
    success_message = 'Seus dados foram cadastrados conforme preencimento do formulário.'

class TipoClinicaUpdateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, UpdateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = TipoClinica
    template_name = 'saude_cadastro/tipoclinica_create_update_form.html'
    form_class = TipoClinicaForm
    success_url = reverse_lazy('saude_cadastro:tipoclinica_list')

class TipoClinicaDeleteView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, DeleteView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = TipoClinica
    template_name = "saude_cadastro/tipoclinica.html"
    success_url = reverse_lazy('saude_cadastro:tipoclinica_list')

class ConvenioListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = Convenio
    template_name = 'saude_cadastro/convenio.html'
    paginate_by=10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('nome')

        if self.request.GET.get("nome_filtro"):
            queryset = queryset.filter(nome__icontains=self.request.GET.get("nome_filtro"))
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['nome_filtro'] = self.request.GET.get('nome_filtro', "")

        context['crumbs'] = [
            {'label': 'Listagem de Convênios', 'url': reverse('saude_cadastro:convenio_list')}
        ]

        return context

class ConvenioCreateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, CreateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = Convenio
    template_name = 'saude_cadastro/convenio_create_update_form.html'
    form_class = ConvenioForm
    success_url = reverse_lazy('saude_cadastro:convenio_list')
    success_message = 'Seus dados foram cadastrados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['crumbs'] = [
            {'label': 'Listagem de Convênios', 'url': reverse('saude_cadastro:convenio_list')},
            {'label': 'Cadastro de Convênio', 'url': reverse('saude_cadastro:convenio_add')}
        ]

        return context

class ConvenioUpdateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission , SuccessMessageMixin, UpdateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = Convenio
    template_name = 'saude_cadastro/convenio_create_update_form.html'
    form_class = ConvenioForm
    success_url = reverse_lazy('saude_cadastro:convenio_list')
    success_message = 'Seus dados foram alterados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['crumbs'] = [
            {'label': 'Listagem de Convênios', 'url': reverse('saude_cadastro:convenio_list')},
            {'label': 'Editar dados do convênio', 'url': reverse('saude_cadastro:convenio_update', kwargs={'pk': self.object.pk})}
        ]

        return context

class ConvenioDeleteView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, DeleteView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = Convenio
    template_name = "saude_cadastro/convenio.html"
    success_url = reverse_lazy('saude_cadastro:convenio_list')
    success_message = 'Seus dados foram deletados conforme solicitado.'

class CIDListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = CID
    template_name = 'saude_cadastro/cid.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('codigo')

        if self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "cid":
            queryset = queryset.filter(nome__icontains=self.request.GET.get('buscar_nome'))
        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "codigo":
            queryset = queryset.filter(codigo=self.request.GET.get('buscar_nome'))
      
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['buscar_nome'] = self.request.GET.get('buscar_nome', "")
        context['opcao_filtro'] = self.request.GET.get('opcao_filtro', "") if self.request.GET.get('opcao_filtro', "") else "cid"

        context['crumbs'] = [
            {'label': 'Listagem de CIDs', 'url': reverse('saude_cadastro:cid_list')}
        ]

        return context

class CIDCreateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, CreateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = CID
    template_name = 'saude_cadastro/cid_create_update_form.html'
    form_class = CIDForm
    success_url = reverse_lazy('saude_cadastro:cid_list')
    success_message = 'Seus dados foram cadastrados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['crumbs'] = [
            {'label': 'Listagem de CIDs', 'url': reverse('saude_cadastro:cid_list')},
            {'label': 'Cadastro de CID', 'url': reverse('saude_cadastro:cid_add')}
        ]

        return context

class CIDUpdateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, UpdateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = CID
    template_name = 'saude_cadastro/cid_create_update_form.html'
    form_class = CIDForm
    success_url = reverse_lazy('saude_cadastro:cid_list')
    success_message = 'Seus dados foram alterados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['crumbs'] = [
            {'label': 'Listagem de CIDs', 'url': reverse('saude_cadastro:cid_list')},
            {'label': 'Editar dados do CID', 'url': reverse('saude_cadastro:cid_update', kwargs={'pk': self.object.pk})}
        ]

        return context

class CIDDeleteView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, DeleteView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = CID
    template_name = "saude_cadastro/cid.html"
    success_url = reverse_lazy('saude_cadastro:cid_list')
    success_message = 'Seus dados foram deletados conforme solicitado.'

class DestinoObitoListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = DestinoObito
    context_object_name = 'destinosdeobito'
    template_name = 'saude_cadastro/destino_de_obito.html'
    paginate_by=10

    def get_queryset(self):
        queryset = super().get_queryset().filter(unidade_saude=self.request.user.get_unidade_login().unidade).order_by('nome_destino_obito')

        if self.request.GET.get("nome_destino_obito_filtro"):
            queryset = queryset.filter(nome_destino_obito__icontains=self.request.GET.get("nome_destino_obito_filtro"))
        if self.request.GET.get("situacao_filtro"):
            queryset = queryset.filter(situacao=self.request.GET.get("situacao_filtro"))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['nome_destino_obito_filtro'] = self.request.GET.get('nome_destino_obito_filtro', '')

        context['situacao_filtro'] = ""

        if self.request.GET.get('situacao_filtro', ''):
            context['situacao_filtro'] = self.request.GET.get('situacao_filtro', '')
        
        situacoes = []

        for situacao in DestinoObito.SITUACOES_CHOICES:
            situacoes.append(situacao[1])
        
        context['situacoes'] = situacoes

        context['crumbs'] = [
            {'label': 'Listagem de Destinos de Óbito', 'url': reverse('saude_cadastro:destinoobito_list')}
        ]
        
        return context

class DestinoObitoCreateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, CreateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = DestinoObito
    template_name = 'saude_cadastro/destino_de_obito_create_update_form.html'
    form_class = DestinoObitoForm
    success_url = reverse_lazy('saude_cadastro:destinoobito_list')
    success_message = 'Seus dados foram cadastrados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['crumbs'] = [
            {'label': 'Listagem de Destinos de Óbito', 'url': reverse('saude_cadastro:destinoobito_list')},
            {'label': 'Cadastro de Destino de Óbito', 'url': reverse('saude_cadastro:destinoobito_add')}
        ]

        return context

    def form_valid(self, form):
        form.instance.unidade_saude = self.request.user.get_unidade_login().unidade
        return super().form_valid(form)

class DestinoObitoUpdateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, UpdateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = DestinoObito
    template_name = 'saude_cadastro/destino_de_obito_create_update_form.html'
    form_class = DestinoObitoForm
    success_url = reverse_lazy('saude_cadastro:destinoobito_list')
    success_message = 'Seus dados foram alterados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['crumbs'] = [
            {'label': 'Listagem de Destinos de Óbito', 'url': reverse('saude_cadastro:destinoobito_list')},
            {'label': 'Editar dados do destino de óbito', 'url': reverse('saude_cadastro:destinoobito_update', kwargs={'pk': self.object.pk})}
        ]

        return context

    def form_valid(self, form):
        form.instance.unidade_saude = self.request.user.get_unidade_login().unidade
        return super().form_valid(form)

class DestinoObitoDeleteView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, DeleteView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = DestinoObito
    template_name = "saude_cadastro/destino_de_obito.html"
    success_url = reverse_lazy('saude_cadastro:destinoobito_list')
    success_message = 'Seus dados foram deletados conforme solicitado.'

class TipoExameListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = TipoExame
    context_object_name = 'tiposdeexames'
    template_name = 'saude_cadastro/tipo_de_exames.html'
    paginate_by=10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('nome')

        if self.request.GET.get("nome_filtro"):
            queryset = queryset.filter(nome__icontains=self.request.GET.get("nome_filtro"))
        
        if self.request.GET.get("tipo_filtro"):
            queryset = queryset.filter(tipo=int(self.request.GET.get("tipo_filtro")))

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['nome_filtro'] = self.request.GET.get('nome_filtro', '')

        context['tipo_filtro'] = ""

        if self.request.GET.get('tipo_filtro', ''):
            context['tipo_filtro'] = int(self.request.GET.get('tipo_filtro', ''))

        tipos = []

        for tipo in TipoExame.TIPO_CHOICES:
            tipos.append(tipo[1])
        
        context['tipos'] = tipos

        context['crumbs'] = [
            {'label': 'Listagem de Tipos de Exame', 'url': reverse('saude_cadastro:tipoexame_list')}
        ]

        return context

class TipoExameCreateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, CreateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = TipoExame
    template_name = 'saude_cadastro/tipo_de_exames_create_update_form.html'
    form_class = TipoExameForm
    success_url = reverse_lazy('saude_cadastro:tipoexame_list')
    success_message = 'Seus dados foram cadastrados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['crumbs'] = [
            {'label': 'Listagem de Tipos de Exame', 'url': reverse('saude_cadastro:tipoexame_list')},
            {'label': 'Cadastro de Tipo de Exame', 'url': reverse('saude_cadastro:tipoexame_add')}
        ]

        return context

    def form_valid(self, form):
        form.instance.unidade_saude = self.request.user.profissional_set.first().unidadelogin.unidade
        return super().form_valid(form)

class TipoExameUpdateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, UpdateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = TipoExame
    template_name = 'saude_cadastro/tipo_de_exames_create_update_form.html'
    form_class = TipoExameForm
    success_url = reverse_lazy('saude_cadastro:tipoexame_list')
    success_message = 'Seus dados foram alterados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['crumbs'] = [
            {'label': 'Listagem de Tipos de Exame', 'url': reverse('saude_cadastro:tipoexame_list')},
            {'label': 'Editar dados do tipo de exame', 'url': reverse('saude_cadastro:tipoexame_update', kwargs={'pk': self.object.pk})}
        ]

        return context

class TipoExameDeleteView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, DeleteView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = TipoExame
    template_name = "saude_cadastro/tipo_de_exames.html"
    success_url = reverse_lazy('saude_cadastro:tipoexame_list')
    success_message = 'Seus dados foram deletados conforme solicitado.'

class ExameListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = Exame
    template_name = 'saude_cadastro/exame.html'
    paginate_by=10
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('nome')

        if self.request.GET.get("nome_filtro"):
            queryset = queryset.filter(nome__icontains=self.request.GET.get("nome_filtro"))
        if self.request.GET.get("tipo_exames_filtro"):
            queryset = queryset.filter(tipo_exame__id__exact=self.request.GET.get("tipo_exames_filtro"))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['nome_filtro'] = self.request.GET.get('nome_filtro', '')

        context['tipo_exames_filtro'] = ""

        if self.request.GET.get('tipo_exames_filtro', ''):
            context['tipo_exames_filtro'] = UUID(self.request.GET.get('tipo_exames_filtro', ''))
        
        context['tipos_exames'] = TipoExame.objects.filter()

        context['crumbs'] = [
            {'label': 'Listagem de Exames', 'url': reverse('saude_cadastro:exame_list')}
        ]

        return context

class ExameCreateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, CreateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = Exame
    template_name = 'saude_cadastro/exame_create_update_form.html'
    form_class = ExameForm
    success_url = reverse_lazy('saude_cadastro:exame_list')
    success_message = 'Seus dados foram cadastrados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['crumbs'] = [
            {'label': 'Listagem de Exames', 'url': reverse('saude_cadastro:exame_list')},
            {'label': 'Cadastro de Exame', 'url': reverse('saude_cadastro:exame_add')}
        ]

        return context

class ExameUpdateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, UpdateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = Exame
    template_name = 'saude_cadastro/exame_create_update_form.html'
    form_class = ExameForm
    success_url = reverse_lazy('saude_cadastro:exame_list')
    success_message = 'Seus dados foram alterados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['crumbs'] = [
            {'label': 'Listagem de Exames', 'url': reverse('saude_cadastro:exame_list')},
            {'label': 'Editar dados do exame', 'url': reverse('saude_cadastro:exame_update', kwargs={'pk': self.object.pk})}
        ]

        return context

class ExameDeleteView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, DeleteView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = Exame
    template_name = "saude_cadastro/exame.html"
    success_url = reverse_lazy('saude_cadastro:exame_list')
    success_message = 'Seus dados foram deletados conforme solicitado.'

class TipoClassificacaoRiscoListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = TipoClassificacaoRisco
    context_object_name = 'tiposclassificacaorisco'
    template_name = 'saude_cadastro/tipo_classificacao_risco.html'
    paginate_by=10

    def get_queryset(self):
        queryset = super().get_queryset().filter(unidade_saude=self.request.user.get_unidade_login().unidade).order_by('-ordem')
        
        if self.request.GET.get("tipo_filtro"):
            queryset = queryset.filter(tipo=int(self.request.GET.get("tipo_filtro")))
        if self.request.GET.get("situacao_filtro"):
            queryset = queryset.filter(situacao=int(self.request.GET.get("situacao_filtro")))
        if self.request.GET.get("ordem_filtro"):
            queryset = queryset.filter(ordem=int(self.request.GET.get("ordem_filtro")))

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['ordem_filtro'] = self.request.GET.get('ordem_filtro', '')

        context['tipo_filtro'] = ""

        if self.request.GET.get('tipo_filtro', ''):
            context['tipo_filtro'] = int(self.request.GET.get('tipo_filtro', ''))

        tipos = []

        for tipo in TipoClassificacaoRisco.TIPO_CLASSIFICACAO_RISCO_CHOICES:
            tipos.append(tipo[1])
        
        context['tipos'] = tipos

        context['situacao_filtro'] = ""

        if self.request.GET.get('situacao_filtro', ''):
            context['situacao_filtro'] = int(self.request.GET.get('situacao_filtro', ''))

        situacoes = []

        for situacao in TipoClassificacaoRisco.SITUACAO_CHOICES:
            situacoes.append(situacao[1])
        
        context['situacoes'] = situacoes

        context['crumbs'] = [
            {'label': 'Listagem de Tipos de Classificação de Risco', 'url': reverse('saude_cadastro:tipoclassificacaorisco_list')}
        ]

        return context

class TipoHistoriaClinicaListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = TipoHistoriaClinica
    context_object_name = 'tiposdehistoriaclinica'
    template_name = 'saude_cadastro/tipo_de_historia_clinica.html'
    paginate_by=10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('nome')

        if self.request.GET.get("nome_filtro"):
            queryset = queryset.filter(nome__icontains=self.request.GET.get("nome_filtro"))
        if self.request.GET.get("situacao_filtro"):
            queryset = queryset.filter(situacao=self.request.GET.get("situacao_filtro"))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['nome_filtro'] = self.request.GET.get('nome_filtro', '')

        context['situacao_filtro'] = ""

        if self.request.GET.get('situacao_filtro', ''):
            context['situacao_filtro'] = self.request.GET.get('situacao_filtro', '')

        situacoes = []

        for situacao in TipoHistoriaClinica.SITUACOES_CHOICES:
            situacoes.append(situacao[1])

        context['situacoes'] = situacoes

        context['crumbs'] = [
            {'label': 'Listagem de Tipos de História Clínica', 'url': reverse('saude_cadastro:tipohistoriaclinica_list')}
        ]
       
        return context

class TipoHistoriaClinicaCreateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, CreateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = TipoHistoriaClinica
    template_name = 'saude_cadastro/tipo_de_historia_clinica_create_update_form.html'
    form_class = TipoHistoriaClinicaForm
    success_url = reverse_lazy('saude_cadastro:tipohistoriaclinica_list')
    success_message = 'Seus dados foram cadastrados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['crumbs'] = [
            {'label': 'Listagem de Tipos de História Clínica', 'url': reverse('saude_cadastro:tipohistoriaclinica_list')},
            {'label': 'Cadastro de Tipo de História Clínica', 'url': reverse('saude_cadastro:tipohistoriaclinica_add')}
        ]

        return context

class TipoHistoriaClinicaUpdateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, UpdateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = TipoHistoriaClinica
    template_name = 'saude_cadastro/tipo_de_historia_clinica_create_update_form.html'
    form_class = TipoHistoriaClinicaForm
    success_url = reverse_lazy('saude_cadastro:tipohistoriaclinica_list')
    success_message = 'Seus dados foram alterados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['crumbs'] = [
            {'label': 'Listagem de Tipos de História Clínica', 'url': reverse('saude_cadastro:tipohistoriaclinica_list')},
            {'label': 'Editar dados do tipo de história clínica', 'url': reverse('saude_cadastro:tipohistoriaclinica_update', kwargs={'pk': self.object.pk})}
        ]

        return context

class TipoHistoriaClinicaDeleteView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, DeleteView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = TipoHistoriaClinica
    template_name = "saude_cadastro/tipo_de_historia_clinica.html"
    success_url = reverse_lazy('saude_cadastro:tipohistoriaclinica_list')
    success_message = 'Seus dados foram deletados conforme solicitado.'

class TipoPosologiaListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = TipoPosologia
    context_object_name = 'tiposdeposologia'
    template_name = 'saude_cadastro/tipo_de_posologia.html'
    paginate_by=10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('nome')

        if self.request.GET.get("nome_filtro"):
            queryset = queryset.filter(nome__icontains=self.request.GET.get("nome_filtro"))
        if self.request.GET.get("quantidade_por_dia_filtro"):
            queryset = queryset.filter(quantidade__exact=self.request.GET.get("quantidade_por_dia_filtro"))
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['nome_filtro'] = self.request.GET.get('nome_filtro', '')
        context['quantidade_por_dia_filtro'] = self.request.GET.get('quantidade_por_dia_filtro', '')

        context['crumbs'] = [
            {'label': 'Listagem de Tipos de Posologia', 'url': reverse('saude_cadastro:tipoposologia_list')}
        ]

        return context

class TipoPosologiaCreateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, CreateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = TipoPosologia
    template_name = 'saude_cadastro/tipo_de_posologia_create_update_form.html'
    form_class = TipoPosologiaForm
    success_url = reverse_lazy('saude_cadastro:tipoposologia_list')
    success_message = 'Seus dados foram cadastrados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['crumbs'] = [
            {'label': 'Listagem de Tipos de Posologia', 'url': reverse('saude_cadastro:tipoposologia_list')},
            {'label': 'Cadastro de Tipo de Posologia', 'url': reverse('saude_cadastro:tipoposologia_add')}
        ]

        return context

class TipoPosologiaUpdateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, UpdateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = TipoPosologia
    template_name = 'saude_cadastro/tipo_de_posologia_create_update_form.html'
    form_class = TipoPosologiaForm
    success_url = reverse_lazy('saude_cadastro:tipoposologia_list')
    success_message = 'Seus dados foram alterados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['crumbs'] = [
            {'label': 'Listagem de Tipos de Posologia', 'url': reverse('saude_cadastro:tipoposologia_list')},
            {'label': 'Editar dados do tipo de Posologia', 'url': reverse('saude_cadastro:tipoposologia_update', kwargs={'pk': self.object.pk})}
        ]

        return context

class TipoPosologiaDeleteView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, DeleteView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = TipoPosologia
    template_name = "saude_cadastro/tipo_de_posologia.html"
    success_url = reverse_lazy('saude_cadastro:tipoposologia_list')
    success_message = 'Seus dados foram deletados conforme solicitado.'

class TransporteListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = Transporte
    # context_object_name = 'transportes'
    template_name = 'saude_cadastro/transporte.html'
    paginate_by=10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('nome_transporte')

        if self.request.GET.get("nome_transporte_filtro"):
            queryset = queryset.filter(nome_transporte__icontains=self.request.GET.get("nome_transporte_filtro"))
        if self.request.GET.get("situacao_filtro"):
            queryset = queryset.filter(situacao=self.request.GET.get("situacao_filtro"))
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['nome_transporte_filtro'] = self.request.GET.get('nome_transporte_filtro', '')

        context['situacao_filtro'] = ""

        if self.request.GET.get('situacao_filtro', ''):
            context['situacao_filtro'] = self.request.GET.get('situacao_filtro', '')
        
        situacoes = []

        for situacao in Transporte.SITUACOES_CHOICES:
            situacoes.append(situacao[1])
        
        context['situacoes'] = situacoes

        context['crumbs'] = [
            {'label': 'Listagem de Transportes', 'url': reverse('saude_cadastro:transporte_list')}
        ]
        
        return context

class TransporteCreateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, CreateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = Transporte
    template_name = 'saude_cadastro/transporte_create_update_form.html'
    form_class = TransporteForm
    success_url = reverse_lazy('saude_cadastro:transporte_list')
    success_message = 'Seus dados foram cadastrados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['crumbs'] = [
            {'label': 'Listagem de Transportes', 'url': reverse('saude_cadastro:transporte_list')},
            {'label': 'Cadastro de Transporte', 'url': reverse('saude_cadastro:transporte_add')}
        ]

        return context

class TransporteUpdateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, UpdateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = Transporte
    template_name = 'saude_cadastro/transporte_create_update_form.html'
    form_class = TransporteForm
    success_url = reverse_lazy('saude_cadastro:transporte_list')
    success_message = 'Seus dados foram alterados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['crumbs'] = [
            {'label': 'Listagem de Transportes', 'url': reverse('saude_cadastro:transporte_list')},
            {'label': 'Editar dados do transporte', 'url': reverse('saude_cadastro:transporte_update', kwargs={'pk': self.object.pk})}
        ]

        return context

class TransporteDeleteView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, DeleteView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = Transporte
    template_name = "saude_cadastro/transporte.html"
    success_url = reverse_lazy('saude_cadastro:transporte_list')
    success_message = 'Seus dados foram deletados conforme solicitado.'

class SalaListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = Sala
    context_object_name = 'salas'
    template_name = 'saude_cadastro/sala.html'
    paginate_by=10

    def get_queryset(self):
        queryset = super().get_queryset().filter(unidade_setor__unidade_saude=self.request.user.get_unidade_login().unidade).order_by('nome_sala')

        if self.request.GET.get("nome_sala_filtro"):
            queryset = queryset.filter(nome_sala__icontains=self.request.GET.get("nome_sala_filtro"))
        if self.request.GET.get("setor_filtro"):
            queryset = queryset.filter(unidade_setor__id__exact=self.request.GET.get("setor_filtro"))
        if self.request.GET.get("situacao_filtro"):
            queryset = queryset.filter(situacao=int(self.request.GET.get("situacao_filtro")))
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['nome_sala_filtro'] = self.request.GET.get('nome_sala_filtro', '')

        context['situacao_filtro'] = ""

        if self.request.GET.get('situacao_filtro', ''):
            context['situacao_filtro'] = int(self.request.GET.get('situacao_filtro', ''))

        situacoes = []

        for situacao in Sala.SITUACAO_CHOICES:
            situacoes.append(situacao[1])
        
        context['situacoes'] = situacoes

        context['setor_filtro'] = ""

        if self.request.GET.get('setor_filtro', ''):
            context['setor_filtro'] = UUID(self.request.GET.get('setor_filtro', ''))
        
        context['setores'] = UnidadeSetor.objects.filter(unidade_saude=self.request.user.get_unidade_login().unidade, situacao=UnidadeSetor.ATIVO)

        context['crumbs'] = [
            {'label': 'Listagem de Salas', 'url': reverse('saude_cadastro:sala_list')}
        ]
        
        return context

class SalaCreateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, CreateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = Sala
    template_name = 'saude_cadastro/sala_create_update_form.html'
    form_class = SalaForm
    success_url = reverse_lazy('saude_cadastro:sala_list')
    success_message = 'Seus dados foram cadastrados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        forms = self.form_class()

        forms.fields["unidade_setor"].queryset = UnidadeSetor.objects.filter(unidade_saude=self.request.user.get_unidade_login().unidade)

        context["form"] = forms

        context['crumbs'] = [
            {'label': 'Listagem de Salas', 'url': reverse('saude_cadastro:sala_list')},
            {'label': 'Cadastro de Sala', 'url': reverse('saude_cadastro:sala_add')}
        ]

        return context

    def form_valid(self, form):
        form.instance.unidade_setor = form.cleaned_data.get('unidade_setor')
        return super().form_valid(form)

class SalaUpdateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, UpdateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = Sala
    template_name = 'saude_cadastro/sala_create_update_form.html'
    form_class = SalaForm
    success_url = reverse_lazy('saude_cadastro:sala_list')
    success_message = 'Seus dados foram alterados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form"].fields["unidade_setor"].queryset = UnidadeSetor.objects.filter(unidade_saude=self.request.user.get_unidade_login().unidade)

        context['crumbs'] = [
            {'label': 'Listagem de Salas', 'url': reverse('saude_cadastro:sala_list')},
            {'label': 'Editar dados da sala', 'url': reverse('saude_cadastro:sala_update', kwargs={'pk': self.object.pk})}
        ]

        return context

    def form_valid(self, form):
        form.instance.unidade_setor = form.cleaned_data.get('unidade_setor')
        return super().form_valid(form)

class SalaDeleteView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, DeleteView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = Sala
    template_name = "saude_cadastro/sala.html"
    success_url = reverse_lazy('saude_cadastro:sala_list')
    success_message = 'Seus dados foram deletados conforme solicitado.'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', None)

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, self.success_message)
            
        except ProtectedError:
            messages.error(self.request, "Ocorreu um erro ao remover, não é possível remover a sala que está vinculada.")
            
        return HttpResponseRedirect(self.get_success_url())

class ProfissionalListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = Profissional
    # context_object_name = 'profissionais'
    template_name = 'saude_cadastro/profissional.html'
    paginate_by=10
    
    def get_queryset(self):
        # queryset = super().get_queryset().filter(unidade_saude=self.request.user.get_unidade_login().unidade).order_by('nome_profissional')
        queryset = super().get_queryset().order_by('nome_profissional')

        if self.request.GET.get("nome_profissional_filtro"):
            queryset = queryset.filter(nome_profissional__icontains=self.request.GET.get("nome_profissional_filtro"))
        
        if self.request.GET.get("crm_filtro"):
            queryset = queryset.filter(crm=self.request.GET.get("crm_filtro"))
        
        if self.request.GET.get("coren_filtro"):
            queryset = queryset.filter(coren=self.request.GET.get("coren_filtro"))

        if self.request.GET.get("cns_filtro"):
            queryset = queryset.filter(cns=self.request.GET.get("cns_filtro"))
        
        if self.request.GET.get("cbo_filtro"):
            queryset = queryset.filter(cbo=self.request.GET.get("cbo_filtro"))
        
        if self.request.GET.get("tipo_profissional_filtro"):
            queryset = queryset.filter(tipo_profissional=int(self.request.GET.get("tipo_profissional_filtro")))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['nome_profissional_filtro'] = self.request.GET.get('nome_profissional_filtro', '')
        context['crm_filtro'] = self.request.GET.get('crm_filtro', '')
        context['coren_filtro'] = self.request.GET.get('coren_filtro', '')
        context['cns_filtro'] = self.request.GET.get('cns_filtro', '')
        context['cbo_filtro'] = self.request.GET.get('cbo_filtro', '')

        context['tipo_profissional_filtro'] = ""

        if self.request.GET.get('tipo_profissional_filtro', ''):
            context['tipo_profissional_filtro'] = int(self.request.GET.get('tipo_profissional_filtro', ''))

        tipos_profissional = []

        for tipo_profissional in Profissional.TIPO_PROFISSIONAL_CHOICES:
            tipos_profissional.append(tipo_profissional[1])
        
        context['tipos_profissional'] = tipos_profissional
        

        context["profissionais"] = self.get_queryset()

        context['crumbs'] = [
            {'label': 'Listagem de Profissionais', 'url': reverse('saude_cadastro:profissional_list')}
        ]

        return context

class ProfissionalCreateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, CreateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = Profissional
    template_name = 'saude_cadastro/profissional_create_update_form.html'
    form_class = ProfissionalForm
    success_url = reverse_lazy('saude_cadastro:profissional_list')
    success_message = 'Seus dados foram cadastrados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["Unidade_saude"] = UnidadeSaude.objects.all()

        context['crumbs'] = [
            {'label': 'Listagem de Profissionais', 'url': reverse('saude_cadastro:profissional_list')},
            {'label': 'Cadastro de Profissional', 'url': reverse('saude_cadastro:profissional_add')}
        ]

        return context

    def form_valid(self, form):
        nome_profissional = form.cleaned_data.get('nome_profissional')
        email = form.cleaned_data.get('email')
        cpf = form.cleaned_data.get('cpf')
        senha = form.cleaned_data.get('senha')
        cpf_replace = cpf.replace('.', '').replace('-', '')

        usuario = Usuario.objects.create_user(cpf_cnpj=cpf_replace, email=email, nome=nome_profissional, password=str(senha))
        usuario. deve_mudar_senha=True
        usuario.save()
        
        self.object = form.save(commit=False)
        self.object.cpf = cpf_replace
        self.object.user = usuario

        return super().form_valid(form)

class ProfissionalUpdateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, UpdateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = Profissional
    template_name = 'saude_cadastro/profissional_create_update_form.html'
    form_class = ProfissionalUpdateViewForm
    success_url = reverse_lazy('saude_cadastro:profissional_list')
    success_message = 'Seus dados foram alterados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["Unidade_saude"] = UnidadeSaude.objects.all()

        context['crumbs'] = [
            {'label': 'Listagem de Profissionais', 'url': reverse('saude_cadastro:profissional_list')},
            {'label': 'Editar dados do profissional', 'url': reverse('saude_cadastro:profissional_update', kwargs={'pk': self.object.pk})}
        ]
        # reverse('saude_atendimento:agenda_medica_medico_view', kwargs={'medico_id': medico_id})

        return context

    def form_valid(self, form):
        nome_profissional = form.cleaned_data.get('nome_profissional')
        email = form.cleaned_data.get('email')
        cpf = form.cleaned_data.get('cpf')
        senha = form.cleaned_data.get('senha')
        cpf_replace = cpf.replace('.', '').replace('-', '')

        # Acesse o usuário associado ao Profissional sendo atualizado
        profissional = get_object_or_404(Profissional, pk=self.kwargs['pk'])
        usuario = profissional.user

        if usuario:
            usuario.email = email
            usuario.cpf_cnpj = cpf_replace
            usuario.nome = nome_profissional
            if senha:
                usuario.set_password(senha)
            usuario.save()

        self.object = form.save(commit=False)
        self.object.cpf = cpf_replace
        self.object.save()

        return super().form_valid(form)
    
class ProfissionalDeleteView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, DeleteView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = Profissional
    template_name = "profissional.html"
    success_url = reverse_lazy('saude_cadastro:profissional_list')
    success_message = 'Seus dados foram deletados conforme solicitado.'

    def form_valid(self, form):
        try:
            user = Usuario.objects.filter(pk=self.object.user.pk)
            user.delete()
            messages.success(self.request, self.success_message)
            
        except ProtectedError:
            messages.error(self.request, "Ocorreu um erro ao remover, existe registros vinculados a esse profissional")
            
        return HttpResponseRedirect(self.get_success_url())

class SetorListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = UnidadeSetor
    context_object_name = 'setores'
    template_name = 'saude_cadastro/setor.html'
    paginate_by=10
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(unidade_saude=self.request.user.profissional_set.first().unidadelogin.unidade).order_by('codigo')

        if self.request.GET.get("nome_filtro"):
            queryset = queryset.filter(nome__icontains=self.request.GET.get("nome_filtro"))
        
        if self.request.GET.get("codigo_filtro"):
            queryset = queryset.filter(codigo=self.request.GET.get("codigo_filtro"))
        
        if self.request.GET.get("sigla_filtro"):
            queryset = queryset.filter(sigla=self.request.GET.get("sigla_filtro"))
        
        if self.request.GET.get("situacao_filtro"):
            queryset = queryset.filter(situacao=self.request.GET.get("situacao_filtro"))
        
        if self.request.GET.get("setor_superior_filtro"):
            queryset = queryset.filter(superior__id__exact=self.request.GET.get("setor_superior_filtro"))

        if self.request.GET.get("recebe_paciente_filtro") == 'SIM':
            queryset = queryset.filter(recebe_paciente=True)
        elif self.request.GET.get("recebe_paciente_filtro") == 'NÃO':
            queryset = queryset.filter(recebe_paciente=False)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['nome_filtro'] = self.request.GET.get('nome_filtro', '')
        context['codigo_filtro'] = self.request.GET.get('codigo_filtro', '')
        context['sigla_filtro'] = self.request.GET.get('sigla_filtro', '')

        context['situacao_filtro'] = ""

        if self.request.GET.get('situacao_filtro', ''):
            context['situacao_filtro'] = int(self.request.GET.get('situacao_filtro', ''))

        situacoes = []

        for situacao in UnidadeSetor.SITUACAO_CHOICES:
            situacoes.append(situacao[1])
        
        context['situacoes'] = situacoes
        context['setor_superior_filtro'] = ""

        if self.request.GET.get('setor_superior_filtro', ''):
            context['setor_superior_filtro'] = UUID(self.request.GET.get('setor_superior_filtro', ''))
        
        context['listagem_select_setores_busca'] = UnidadeSetor.objects.filter(unidade_saude=self.request.user.get_unidade_login().unidade, situacao=UnidadeSetor.ATIVO)
        context['recebe_paciente_filtro'] = self.request.GET.get('recebe_paciente_filtro', '')
        context['listagem_select_recebe_paciente_busca'] = ['SIM', 'NÃO']
        context["setores"] = self.get_queryset()

        context['crumbs'] = [
            {'label': 'Listagem de Setores', 'url': reverse('saude_cadastro:setor_list')}
        ]

        return context

class SetorCreateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, CreateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = UnidadeSetor
    template_name = 'saude_cadastro/setor_create_update_form.html'
    form_class = SetorForm
    success_url = reverse_lazy('saude_cadastro:setor_list')
    success_message = 'Seus dados foram cadastrado conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        forms = self.form_class()

        forms.fields["superior"].queryset = UnidadeSetor.objects.filter(unidade_saude=self.request.user.get_unidade_login().unidade)

        context["form"] = forms

        context['crumbs'] = [
            {'label': 'Listagem de Setores', 'url': reverse('saude_cadastro:setor_list')},
            {'label': 'Cadastro de Setor', 'url': reverse('saude_cadastro:setor_add')}
        ]

        return context

    def form_valid(self, form):
        form.instance.unidade_saude = self.request.user.profissional_set.first().unidadelogin.unidade
        return super().form_valid(form)

class SetorUpdateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, UpdateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = UnidadeSetor
    template_name = 'saude_cadastro/setor_create_update_form.html'
    form_class = SetorForm
    success_url = reverse_lazy('saude_cadastro:setor_list')
    success_message = 'Seus dados foram alterados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form"].fields["superior"].queryset = UnidadeSetor.objects.filter(unidade_saude=self.request.user.get_unidade_login().unidade)

        context['crumbs'] = [
            {'label': 'Listagem de Setores', 'url': reverse('saude_cadastro:setor_list')},
            {'label': 'Editar dados do setor', 'url': reverse('saude_cadastro:setor_update', kwargs={'pk': self.object.pk})}
        ]

        return context

    def form_valid(self, form):
        form.instance.unidade_saude = self.request.user.profissional_set.first().unidadelogin.unidade
        return super().form_valid(form)

class SetorDeleteView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, DeleteView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = UnidadeSetor
    template_name = "saude_cadastro/setor.html"
    success_url = reverse_lazy('saude_cadastro:setor_list')
    success_message = 'Seus dados foram deletados conforme solicitado.'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', None)

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, self.success_message)
            
        except ProtectedError:
            messages.error(self.request, "Ocorreu um erro ao remover, não é possível remover o setor que está vinculado.")
            
        return HttpResponseRedirect(self.get_success_url())
    
class PainelChamadaListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    required_permissions = [settings.DESENVOLVEDOR, settings.RECEPCIONISTA , settings.ADMINISTRADO, settings.PAINEL, settings.MEDICO]
    model = PainelChamada
    template_name = 'saude_cadastro/painel_chamada_list.html'
    paginate_by=10

    def get_queryset(self):
        queryset = super().get_queryset().filter(unidade_saude=self.request.user.get_unidade_login().unidade).order_by('nome')

        if self.request.GET.get("nome_filtro"):
            queryset = queryset.filter(nome__icontains=self.request.GET.get("nome_filtro"))
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_filtro'] = self.request.GET.get('nome_filtro', "")

        context['crumbs'] = [
            {'label': 'Listagem de Painéis', 'url': reverse('saude_cadastro:painel_chamada_list')}
        ]

        return context

class PainelChamadaCreateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, CreateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = PainelChamada
    template_name = 'saude_cadastro/painel_chamada_create_update.html'
    form_class = PainelChamadaForm
    success_url = reverse_lazy('saude_cadastro:painel_chamada_list')
    success_message = 'Seus dados foram cadastrados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["setores"] = UnidadeSetor.objects.filter(unidade_saude=self.request.user.get_unidade_login().unidade)

        context['crumbs'] = [
            {'label': 'Listagem de Painéis', 'url': reverse('saude_cadastro:painel_chamada_list')},
            {'label': 'Cadastro de Painel', 'url': reverse('saude_cadastro:painel_chamada_add')}
        ]

        return context

    def form_valid(self, form):
        form.instance.unidade_saude = self.request.user.profissional_set.first().unidadelogin.unidade
        return super().form_valid(form)
    
class PainelChamadaUpdateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, UpdateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = PainelChamada
    template_name = 'saude_cadastro/painel_chamada_create_update.html'
    form_class = PainelChamadaForm
    success_url = reverse_lazy('saude_cadastro:painel_chamada_list')
    success_message = 'Seus dados foram alterados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["setores"] = UnidadeSetor.objects.filter(unidade_saude=self.request.user.get_unidade_login().unidade)

        context['crumbs'] = [
            {'label': 'Listagem de Painéis', 'url': reverse('saude_cadastro:painel_chamada_list')},
            {'label': 'Editar dados do painel', 'url': reverse('saude_cadastro:painel_chamada_update', kwargs={'pk': self.object.pk})}
        ]

        return context

class PainelChamadaDeleteView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, SuccessMessageMixin, DeleteView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.SUPORTE]
    model = PainelChamada
    template_name = "saude_cadastro/painel_chamada_list.html"
    success_url = reverse_lazy('saude_cadastro:painel_chamada_list')
    success_message = 'Seus dados foram deletados conforme solicitado.'