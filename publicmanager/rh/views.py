from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from publicmanager.comum.models import Municipio
from publicmanager.autenticacao.models import Usuario
from .models import Servidor, PessoaFisica, PessoaJuridica, CargoEmprego, Funcao, JornadaTrabalho, RegimeJuridico, \
    NivelEscolaridade, Situacao
from .forms import ServidorForm, PessoaFisicaForm, PessoaJuridicaForm, CargoEmpregoForm, FuncaoForm, \
    JornadaTrabalhoForm, RegimeJuridicoForm, NivelEscolaridadeForm, SituacaoForm


# Create your views here.
class CargoEmpregoListView(LoginRequiredMixin, ListView):
    model = CargoEmprego
    context_object_name = 'cargos'
    template_name = 'rh/cargos.html'


class CargoEmpregoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = CargoEmprego
    template_name = 'rh/cargo_create_update_form.html'
    form_class = CargoEmpregoForm
    success_url = '/rh/cargo/'
    success_message = 'Seus dados foram cadastrados conforme preencimento do formulário.'


class CargoEmpregoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CargoEmprego
    template_name = 'rh/cargo_create_update_form.html'
    form_class = CargoEmpregoForm
    success_url = '/rh/cargo/'
    success_message = 'Seus dados foram atualizados conforme preencimento do formulário.'


class CargoEmpregoDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = CargoEmprego
    template_name = "rh/cargos.html"
    success_url = '/rh/cargo/'
    success_message = 'Seus dados foram deletados conforme solicitado.'


class FuncaoListView(LoginRequiredMixin, ListView):
    model = Funcao
    context_object_name = 'funcoes'
    template_name = 'rh/funcoes.html'


class FuncaoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Funcao
    template_name = 'rh/funcao_create_update_form.html'
    form_class = FuncaoForm
    success_url = '/rh/funcao'
    success_message = 'Seus dados foram cadastrados conforme preencimento do formulário.'


class FuncaoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Funcao
    template_name = 'rh/funcao_create_update_form.html'
    form_class = FuncaoForm
    success_url = '/rh/funcao'
    success_message = 'Seus dados foram atualizados conforme preencimento do formulário.'


class FuncaoDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Funcao
    template_name = "rh/funcoes.html"
    success_url = '/rh/funcao'
    success_message = 'Seus dados foram deletados conforme solicitado.'


class JornadaTrabalhoListView(LoginRequiredMixin, ListView):
    model = JornadaTrabalho
    context_object_name = 'jornadas_trabalho'
    template_name = 'rh/jornadas_trabalho.html'


class JornadaTrabalhoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = JornadaTrabalho
    template_name = 'rh/jornada_trabalho_create_update_form.html'
    form_class = JornadaTrabalhoForm
    success_url = '/rh/jornada_trabalho'
    success_message = 'Seus dados foram cadastrados conforme preencimento do formulário.'


class JornadaTrabalhoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = JornadaTrabalho
    template_name = 'rh/jornada_trabalho_create_update_form.html'
    form_class = JornadaTrabalhoForm
    success_url = '/rh/jornada_trabalho'
    success_message = 'Seus dados foram atualizados conforme preencimento do formulário.'


class JornadaTrabalhoDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = JornadaTrabalho
    template_name = "rh/jornadas_trabalho.html"
    success_url = '/rh/jornadatrabalho'
    success_message = 'Seus dados foram deletados conforme solicitado.'


class RegimeJuridicoListView(LoginRequiredMixin, ListView):
    model = RegimeJuridico
    context_object_name = 'regimes_juridicos'
    template_name = 'rh/regimes_juridicos.html'


class RegimeJuridicoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = RegimeJuridico
    template_name = 'rh/regime_juridico_create_update_form.html'
    form_class = RegimeJuridicoForm
    success_url = '/rh/regime_juridico'
    success_message = 'Seus dados foram cadastrados conforme preencimento do formulário.'


class RegimeJuridicoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = RegimeJuridico
    template_name = 'rh/regime_juridico_create_update_form.html'
    form_class = RegimeJuridicoForm
    success_url = '/rh/regime_juridico'
    success_message = 'Seus dados foram atualizados conforme preencimento do formulário.'


class RegimeJuridicoDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = RegimeJuridico
    template_name = "rh/regimes_juridicos.html"
    success_url = '/rh/regime_juridico'
    success_message = 'Seus dados foram deletados conforme solicitado.'


class NivelEscolaridadeListView(LoginRequiredMixin, ListView):
    model = NivelEscolaridade
    context_object_name = 'niveis_escolaridade'
    template_name = 'rh/niveis_escolaridade.html'


class NivelEscolaridadeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = NivelEscolaridade
    template_name = 'rh/nivel_escolaridade_create_update_form.html'
    form_class = NivelEscolaridadeForm
    success_url = '/rh/nivel_escolaridade'
    success_message = 'Seus dados foram cadastrados conforme preencimento do formulário.'


class NivelEscolaridadeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = NivelEscolaridade
    template_name = 'rh/nivel_escolaridade_create_update_form.html'
    form_class = NivelEscolaridadeForm
    success_url = '/rh/nivel_escolaridade'
    success_message = 'Seus dados foram atualizados conforme preencimento do formulário.'


class NivelEscolaridadeDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = NivelEscolaridade
    template_name = "rh/niveis_escolaridade.html"
    success_url = '/rh/nivel_escolaridade'
    success_message = 'Seus dados foram deletados conforme solicitado.'

class SituacaoListView(LoginRequiredMixin, ListView):
    model = Situacao
    context_object_name = 'situacoes'
    template_name = 'rh/situacoes.html'


class SituacaoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Situacao
    template_name = 'rh/situacao_create_update_form.html'
    form_class = SituacaoForm
    success_url = '/rh/situacao'
    success_message = 'Seus dados foram cadastrados conforme preencimento do formulário.'


class SituacaoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Situacao
    template_name = 'rh/situacao_create_update_form.html'
    form_class = SituacaoForm
    success_url = '/rh/situacao'
    success_message = 'Seus dados foram atualizados conforme preencimento do formulário.'


class SituacaoDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Situacao
    template_name = "rh/situacoes.html"
    success_url = '/rh/situacao'
    success_message = 'Seus dados foram deletados conforme solicitado.'


class PessoaFisicaListView(LoginRequiredMixin, ListView):
    model = PessoaFisica
    context_object_name = 'pessoas'
    template_name = 'rh/pessoafisica.html'


class PessoaFisicaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = PessoaFisica
    template_name = 'rh/pessoafisica_create_update_form.html'
    form_class = PessoaFisicaForm
    success_url = 'rh/pessoa/'
    success_message = 'Seus dados foram cadastrados conforme preencimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nascimento_municipio'] = Municipio.objects.all()

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form_is_valid = form.is_valid()
        if form_is_valid:
            usuario = Usuario.objects.filter(cpf_cnpj=form.cleaned_data["cpf"])
            form.save()
            if not usuario:
                usuario = Usuario(cpf_cnpj=form.cleaned_data["cpf"],
                                  email=form.cleaned_data["email"],
                                  nome=form.cleaned_data["nome_usual"],
                                  )
                usuario.set_password(form.cleaned_data['cpf'])
                usuario.save()
                pessoa = PessoaFisica.objects.get(cpf=form.cleaned_data['cpf'])
                pessoa.user_id = usuario.id
                pessoa.save()
            else:
                pessoa = PessoaFisica.objects.get(cpf=form.cleaned_data['cpf'])
                pessoa.user_id = usuario[0].id
                pessoa.save()

            return redirect('pessoafisica_list')

        return super().post(request, *args, **kwargs)

class PessoaFisicaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = PessoaFisica
    template_name = 'rh/pessoafisica_create_update_form.html'
    form_class = PessoaFisicaForm
    success_url = '/rh/pessoafisica/'
    success_message = 'Seus dados foram atualizados conforme preencimento do formulário.'

class PessoaFisicaDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = PessoaFisica
    template_name = "rh/pessoafisica.html"
    success_url = '/rh/pessoafisica/'
    success_message = 'Seus dados foram deletados conforme solicitado.'


class PessoaJuridicaListView(LoginRequiredMixin, ListView):
    model = PessoaJuridica
    context_object_name = 'pessoasjuridica'
    template_name = 'rh/pessoa_juridica.html'

class PessoaJuridicaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = PessoaJuridica
    template_name = 'rh/pessoa_juridica_create_update_form.html'
    form_class = PessoaJuridicaForm
    success_url = '/rh/pessoajuridica/'
    success_message = 'Seus dados foram cadastrados conforme preencimento do formulário.'


class PessoaJuridicaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = PessoaJuridica
    template_name = 'rh/pessoa_juridica_create_update_form.html'
    form_class = PessoaJuridicaForm
    success_url = '/rh/pessoajuridica/'
    success_message = 'Seus dados foram atualizados conforme preencimento do formulário.'


class PessoaJuridicaDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = PessoaJuridica
    template_name = "rh/pessoa_juridica.html"
    success_url = '/rh/pessoajuridica/'
    success_message = 'Seus dados foram deletados conforme solicitado.'


class ServidorListView(LoginRequiredMixin, ListView):
    model = Servidor
    context_object_name = 'servidores'
    template_name = 'rh/servidores.html'


class ServidorCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Servidor
    template_name = 'rh/servidor_create_update_form.html'
    form_class = ServidorForm
    success_url = '/rh/servidor/'
    success_message = 'Seus dados foram cadastrados conforme preencimento do formulário.'

class ServidorUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Servidor
    template_name = 'rh/servidor_create_update_form.html'
    form_class = ServidorForm
    success_url = '/rh/servidor/'
    success_message = 'Seus dados foram atualizados conforme preencimento do formulário.'
