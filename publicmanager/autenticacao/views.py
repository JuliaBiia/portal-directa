from django.views import View
from django.conf import settings
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login, update_session_auth_hash

from .forms import SaudeLoginForm, AlterarSenhaCriarForm
from publicmanager.saude_cadastro.models import Profissional
from publicmanager.autenticacao.utils import registrar_acesso
from publicmanager.autenticacao.models import PainelUnidadeUsuario, Usuario
from publicmanager.saude.models import UnidadeLogin, UnidadeSaude, EsqueceuSenha

@csrf_exempt
def saude_login_view(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        password = request.POST.get('password')
        unidade_saude_id = request.POST.get('unidades')

        user = authenticate(request, cpf_cnpj=cpf, password=password)
        
        if not user and Usuario.objects.filter(cpf_cnpj=cpf).exists():
            messages.error(request, 'Usuário ou senha inválidos!')
            return redirect('autenticacao:login')

        painel_unidade_usuario = PainelUnidadeUsuario.objects.filter(usuario=user).first()
        
        if painel_unidade_usuario:
            unidade = painel_unidade_usuario.unidade
            login(request, user)
            registrar_acesso(request, user, True, 'Usuário painel autenticado')

            return redirect('saude_cadastro:painel_chamada_list')
        
        try:
            profissional = Profissional.objects.get(cpf=cpf)
        except Profissional.DoesNotExist:
            messages.warning(request, 'Seu cadastro não foi encontrado. Por favor, entre em contato com o administrador da unidade.')
            return redirect('autenticacao:login')

        try:
            unidade = UnidadeSaude.objects.get(pk=unidade_saude_id)
        except UnidadeSaude.DoesNotExist:
            messages.warning(request, 'Você não possui uma unidade configurada para acesso.')
            return redirect('autenticacao:login')

        unidade_saude, created = UnidadeLogin.objects.get_or_create(
            profissional=profissional,
            defaults={'unidade': unidade}
        )
        unidade_saude.unidade = unidade
        unidade_saude.save()

        request.session.set_expiry(28800)

        login(request, user)
        registrar_acesso(request, user, True, 'Usuário autenticado')

        if user.is_staff or (user.tipo_usuario and user.is_staff):
            return redirect('/admin')
        
        if not user.is_staff and user.tipo_usuario:
            return redirect('dashboard:saude_redirect_dashboard')

        messages.error(request, 'Usuário ou senha inválidos!')
        return redirect('autenticacao:login')

    else:
        if request.user.is_authenticated:
            if request.user.is_staff or (request.user.tipo_usuario and request.user.is_staff):
                return redirect('/admin')

            registrar_acesso(request, request.user, True, 'Usuário logado e redirecionado')
            return redirect('dashboard:saude_redirect_dashboard')

        form = SaudeLoginForm()

    return render(request, 'autenticacao/login.html', {'form': form})

class AlterarSenhaView(LoginRequiredMixin, View):
    template_name = 'autenticacao/mudar_senha.html'

    def get(self, request, *args, **kwargs):
        context = {}
        form = PasswordChangeForm(user=request.user)
        context['must_change_password'] = request.session.get('must_change_password', False)
        context['hide_navbar'] = request.session.get('must_change_password', False)
        context['form'] = form

        context['crumbs'] = [
            {'label': 'Alterar Senha', 'url': reverse('autenticacao:alterar_senha')},
        ]

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Senha alterada com sucesso!')
            update_session_auth_hash(request, form.user)
            request.session['must_change_password'] = False
            request.user.must_change_password = False
            request.user.deve_mudar_senha = False
            request.user.save()

            if request.user.tipo_usuario == settings.PAINEL:
                return redirect('saude_cadastro:painel_chamada_list')
            
            return redirect('dashboard:index')
        
        context = {}
        context['must_change_password'] = request.session.get('must_change_password', False)
        context['hide_navbar'] = request.session.get('must_change_password', False)
        context['form'] = form

        context['crumbs'] = [
            {'label': 'Página inicial', 'url': reverse('dashboard:index')},
            {'label': 'Alterar Senha', 'url': reverse('autenticacao:alterar_senha')},
        ]

        return render(request, self.template_name, context)

class AlterarSenhaCreateView(SuccessMessageMixin, CreateView):
    model = EsqueceuSenha
    template_name = 'autenticacao/esqueceu_senha.html'
    form_class = AlterarSenhaCriarForm
    success_url = reverse_lazy('autenticacao:login')
    success_message = 'Sua solicitação foi encaminhada com sucesso! Em breve, entraremos em contato via WhatsApp.'
