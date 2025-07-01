from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, DetailView, UpdateView

from .forms import MeuPerfilUpdateForm
from publicmanager.saude.models import UnidadeSaude
from publicmanager.comum.utils import CheckUserTypeMixin
from publicmanager.dashboard.utils import SaudeCheckHasPermission
from publicmanager.saude_cadastro.models import PainelChamada, Profissional

@login_required
def saude_redirect_dashboard(request):    
    if request.user and request.user.is_anonymous:
        return redirect('autenticacao:login')
    
    ## Usuário não autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('autenticacao:login'))
    
    ## Deve mudar a senha no próximo acesso
    if not request.user.is_anonymous and request.user and request.user.deve_mudar_senha:
        return redirect("autenticacao:alterar_senha")
    
    unidade_login = request.user.get_unidade_login()

    ## Desenvolvedor
    if request.user.tipo_usuario == settings.DESENVOLVEDOR:

        if unidade_login.sala and unidade_login.unidade != unidade_login.sala.unidade_setor.unidade_saude:
            unidade_login.sala = None
            unidade_login.save()
            
        return redirect("dashboard:index")
    
    ## Médico
    if request.user.tipo_usuario == settings.MEDICO:
        
        if not unidade_login.sala:
            messages.warning(request, 'Selecione uma sala antes de iniciar os atendimentos!')

            url = reverse_lazy('saude:selecao_salas_list')
            url_param= f"{url}?inicial=1&setor=1"
            return redirect(url_param)
        
        elif unidade_login.unidade != unidade_login.sala.unidade_setor.unidade_saude:
            unidade_login.sala = None
            unidade_login.save()
            
            messages.warning(request, 'Você precisa selecionar uma sala antes de iniciar os atendimentos!')
            url = reverse_lazy('saude:selecao_salas_list')
            url_param= f"{url}?inicial=1&setor=1"
            return redirect(url_param)
        
        return redirect("saude_atendimento:atendimento_medico_list")
    
    if request.user.tipo_usuario ==  settings.RECEPCIONISTA:
        url = reverse_lazy("saude_atendimento:admissao_paciente_list")
        url_param= f"{url}?modulo=urgencia"
        return redirect(url_param)
        
    return redirect("dashboard:index")

class IndexxView(LoginRequiredMixin, CheckUserTypeMixin, TemplateView):
    login_url = 'auth/login'
    template_name = 'base/base.html'

class IndexView(LoginRequiredMixin, CheckUserTypeMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous  and request.user:
            return redirect('autenticacao:login')
    
        if not request.user.is_anonymous and request.user.deve_mudar_senha:
            return redirect("autenticacao:alterar_senha")
            
        return super(IndexView, self).dispatch(request, *args, **kwargs)

class SaudePainelChamadaDetailView(LoginRequiredMixin, CheckUserTypeMixin, SaudeCheckHasPermission, DetailView):
    required_permissions = [settings.DESENVOLVEDOR, settings.RECEPCIONISTA , settings.ADMINISTRADO, settings.PAINEL, settings.MEDICO]
    template_name = "dashboard/saude/painel_atendimento.html"
    queryset = PainelChamada.objects.all()
    slug_url_kwarg = 'slug1'
    slug_url_kwarg2 = 'slug2'

    def dispatch(self, request, *args, **kwargs):
        slug1 = self.kwargs.get(self.slug_url_kwarg)
        slug2 = self.kwargs.get(self.slug_url_kwarg2)

        if not PainelChamada.objects.filter(slug=slug1, unidade_saude__slug=slug2).exists():
            return redirect("autenticacao:login")
            
        return super(SaudePainelChamadaDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        slug1 = self.kwargs.get(self.slug_url_kwarg)
        slug2 = self.kwargs.get(self.slug_url_kwarg2)
        
        context["slug1"] = slug1
        context["slug2"] = slug2
        context['unidade_saude'] = UnidadeSaude.objects.get(slug=slug2)
        
        return context

class MeuPerfilUpdate(LoginRequiredMixin, CheckUserTypeMixin, SuccessMessageMixin, UpdateView):
    model = Profissional
    template_name = 'dashboard/profile_detail.html'
    form_class = MeuPerfilUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['crumbs'] = [
            {'label': 'Meu Perfil', 'url': reverse('dashboard:meu_perfil_atualizar', kwargs={'pk': self.object.pk})}
        ]
        return context

    def form_valid(self, form):
        nome_profissional = form.cleaned_data.get('nome_profissional')
        email = form.cleaned_data.get('email')
        cpf = form.cleaned_data.get('cpf')
        cpf_replace = cpf.replace('.', '').replace('-', '')

        profissional = get_object_or_404(Profissional, pk=self.kwargs['pk'])
        usuario = profissional.user

        if usuario:
            usuario.email = email
            usuario.cpf_cnpj = cpf_replace
            usuario.nome = nome_profissional
            usuario.save()

        self.object = form.save(commit=False)
        self.object.cpf = cpf_replace
        self.object.save()

        messages.success(self.request, 'Seus dados foram alterados conforme preenchimento do formulário.')

        return HttpResponseRedirect(reverse('dashboard:meu_perfil_atualizar', kwargs={'pk': self.object.pk}))