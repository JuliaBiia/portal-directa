from django.utils import timezone
from uuid import UUID
from django.db.models import Q
from django.conf import settings
from django.contrib import messages
from urllib.parse import urlencode
from datetime import datetime as dt
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Case, Value, When, IntegerField, Q
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, TemplateView, View

from publicmanager.comum.utils import CheckUserTypeMixin
from publicmanager.dashboard.utils import SaudeCheckHasPermission
from publicmanager.saude_cadastro.models import Profissional, UnidadeSetor, TipoClassificacaoRisco, Procedimento

from publicmanager.saude_enfermagem.models import (
    ListaChamadoAdministracaoMedicamento, ListaChamadoAdministracaoProcedimento, ReceitaAdministracaoProcedimento,
    AdministracaoProcedimento, SituacaoAdministracaoProcedimento
)
from publicmanager.saude_atendimento.models import (
    Paciente, TipoAltaHospitalar, ListaChamada, ClassificacaoRisco, BoletimPaciente, AtendimentoMedico,
    AtestadoAtendimento, DiagnosticoAtendimento, FichaReferenciaAtendimento, HistoricoEsperaAtendimento,
    ExameAtendimento, MedicacaoAtendimento, JustificativaProcedimentoAtendimento, ProcedimentoAtendimento,
    JustificativaProcedimentoAtendimento, ListaChamadaClassificacaoRisco
)
from publicmanager.saude_atendimento.forms import (
    TipoAltaHospitalarForm, ClassificacaoRiscoCriarForm,
    ClassificacaoRiscoAtualizarForm, PacienteNovoBoletimCreateForm, PacienteNovoBoletimUpdateForm, AtestadoAtendimentoForm,
    FichaReferenciaAtendimentoForm, JustificativaProcedimentoCreateForm, JustificativaProcedimentoUpdateForm
)

import traceback

class PacienteNovoBoletimDetailView(CheckUserTypeMixin, LoginRequiredMixin, DetailView):
    model = Paciente
    context_object_name = "paciente"
    # required_permissions = [settings.DESENVOLVEDOR, settings.RECEPCIONISTA, settings.ADMINISTRADO]
    template_name = "saude_atendimento/urgencia/paciente_novo_boletim.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_atual'] = timezone.now()

        list_url = reverse('saude_atendimento:admissao_paciente_list')

        query_string = None
        if self.request.GET.get('modulo') == 'urgencia':
            query_string = urlencode({'modulo': 'urgencia'})

        elif self.request.GET.get('modulo') == 'consultorio':
            query_string = urlencode({'modulo': 'consultorio'})

        context['crumbs'] = [
            {'label': 'Listagem de Pacientes', 'url': f'{list_url}?{query_string}'},
            {'label': 'Novo Boletim', 'url': '#'},
        ]

        context['boletins'] = BoletimPaciente.objects.filter(
            unidade_saude=self.request.user.get_unidade_login().unidade,
            paciente=self.object.pk, situacao=BoletimPaciente.EM_ABERTO,
        ).order_by('created_at')

        context['modulo'] = self.request.GET.get('modulo', "")

        if self.request.GET.get('boletim'):
            context['boletim_filtro'] = BoletimPaciente.objects.get(pk=self.request.GET.get('boletim'))

        return context
    
class PacienteNovoBoletimCreateView(CheckUserTypeMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = BoletimPaciente
    template_name = 'saude_atendimento/urgencia/paciente_novo_boletim.html'
    form_class = PacienteNovoBoletimCreateForm
    # required_permissions = [settings.DESENVOLVEDOR, settings.RECEPCIONISTA, settings.ADMINISTRADO]
    success_message = 'Seus dados foram cadastrados conforme preencimento do formulário.'

    def form_valid(self, form):
        profissional=Profissional.objects.get(user=self.request.user)
        paciente = form.cleaned_data.get('paciente')
        unidade = profissional.unidadelogin.unidade
        
        self.object = form.save(commit=False)

        if BoletimPaciente.objects.filter(unidade_saude=unidade, paciente=paciente.pk, situacao=BoletimPaciente.EM_ABERTO, tipo=BoletimPaciente.URGENCIA).exists() and self.object.tipo == 0:
            messages.warning(self.request, 'Já existe um boletim do tipo urgência em aberto!')

            url = reverse('saude_atendimento:paciente_boletim_listagem', kwargs = {'pk': paciente.pk})
            url_com_parametro = f"{url}?modulo=urgencia"
            return redirect(url_com_parametro)
        
        elif BoletimPaciente.objects.filter(unidade_saude=unidade, paciente=paciente.pk, situacao=BoletimPaciente.EM_ABERTO, tipo=BoletimPaciente.MEDICACAO).exists() and self.object.tipo == 1:
            messages.warning(self.request, 'Já existe um boletim do tipo medicação em aberto!')

            url = reverse('saude_atendimento:paciente_boletim_listagem', kwargs = {'pk': paciente.pk})
            url_com_parametro = f"{url}?modulo=urgencia"
            return redirect(url_com_parametro)
        
        self.object.unidade_saude=unidade
        self.object.profissional=profissional
        self.object.save()

        if self.object.tipo == BoletimPaciente.MEDICACAO:
            ListaChamadoAdministracaoMedicamento.objects.create(
                boletim=self.object,
                unidade_saude=profissional.unidadelogin.unidade
            )

        url = reverse('saude_atendimento:paciente_boletim_listagem', kwargs = {'pk': paciente.pk})
        url_com_parametro = f"{url}?modulo=urgencia"

        return redirect(url_com_parametro)
        
class PacienteNovoBoletimDeleteView(CheckUserTypeMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = BoletimPaciente
    # required_permissions = [settings.DESENVOLVEDOR, settings.RECEPCIONISTA, settings.ADMINISTRADO]
    template_name = 'saude_atendimento/urgencia/confirmar_cancelar_remocao.html'

    def get_success_url(self):
        if self.request.GET.get('paciente'):
            return reverse('saude_atendimento:paciente_boletim_listagem', kwargs={'pk': self.request.GET.get('paciente')})
    
class PacienteNovoBoletimUpdateView(CheckUserTypeMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = BoletimPaciente
    template_name = 'saude_atendimento/urgencia/paciente_novo_boletim.html'
    form_class = PacienteNovoBoletimUpdateForm
    # required_permissions = [settings.DESENVOLVEDOR, settings.RECEPCIONISTA, settings.ADMINISTRADO]
    success_message = 'Seus dados foram alterados conforme preencimento do formulário.'

    def get_success_url(self):
        if self.request.GET.get('paciente'):
            return reverse('saude_atendimento:paciente_boletim_listagem', kwargs={'pk': self.request.GET.get('paciente')})

class ClassificacaoRiscoListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ENFERMEIRO, settings.TECNICO_ENFERMAGEM, settings.ADMINISTRADO, settings.MEDICO]
    model = ClassificacaoRisco
    template_name = 'saude_atendimento/urgencia/classificacao_risco_list.html'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if not request.user.is_authenticated or request.user.is_anonymous:
            return response
        
        if self.request.user.tipo_usuario in ['desenvolvedor', 'medico', 'enfermeiro', 'tecnico_enfermagem'] and not self.request.user.get_unidade_login().sala:

            messages.warning(request, 'Você precisa selecionar uma sala antes de iniciar os atendimentos!')
            params = {'setor': '15'}
            url = f"{reverse('saude:selecao_salas_list')}?{urlencode(params)}"

            return redirect(url)

        return super(ClassificacaoRiscoListView, self).dispatch(request, *args, **kwargs)
            
    def get_queryset(self):
        queryset = super().get_queryset().filter(
            boletim__unidade_saude=self.request.user.get_unidade_login().unidade,
            boletim__tipo=BoletimPaciente.URGENCIA
        ).order_by('created_at')

        if self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "paciente":
            queryset = queryset.filter(paciente__nome_paciente__icontains=self.request.GET.get('buscar_nome'))
            
        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "cpf":
            queryset = queryset.filter(paciente__cpf=self.request.GET.get('buscar_nome'))

        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "rg":
            queryset = queryset.filter(paciente__rg=self.request.GET.get('buscar_nome'))

        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "sus":
            queryset = queryset.filter(paciente__cartao_sus=self.request.GET.get('buscar_nome'))
      
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        lista_chamada_classificacao = ListaChamadaClassificacaoRisco.objects.filter(
            boletim__boletim_classificacao_risco_set__isnull=True,
            boletim__situacao=BoletimPaciente.EM_ABERTO,
            boletim__tipo=BoletimPaciente.URGENCIA,
            situacao__in=[
                ListaChamadaClassificacaoRisco.CHAMADO,
                ListaChamadaClassificacaoRisco.EM_ATENDIMENTO,
                ListaChamadaClassificacaoRisco.CLASSIFICADO
            ]
        ).order_by('created_at').distinct()

        riscos_classificados = self.get_queryset().filter(
            Q(status=ClassificacaoRisco.ATIVO),
            Q(setor=ClassificacaoRisco.TRIAGEM),
            Q(
                Q(boletim__situacao=BoletimPaciente.EM_ABERTO) |
                Q(classificacao_risco_lista_chamada_set__situacao__in=[ListaChamada.EM_ESPERA, ListaChamada.EM_ATENDIMENTO])
            )
        ).annotate(
            ordenacao_risco=Case(
                When(tipo_classificacao_risco__tipo=4, then=Value(1)),
                When(tipo_classificacao_risco__tipo=3, then=Value(2)),
                When(tipo_classificacao_risco__tipo=2, then=Value(3)),
                When(tipo_classificacao_risco__tipo=1, then=Value(4)),
                When(tipo_classificacao_risco__tipo=0, then=Value(5)),
                default=Value(6),
                output_field=IntegerField(),
            )
        ).order_by('ordenacao_risco').distinct()

        context["lista_chamada_classificacao"] = lista_chamada_classificacao
        context["boletins_pacientes_classificados"] = riscos_classificados
        context["boletins_pacientes_abertos"] = BoletimPaciente.objects.filter(situacao=BoletimPaciente.EM_ABERTO, tipo=BoletimPaciente.URGENCIA, listachamadaclassificacaorisco__isnull=True)
        context['crumbs'] = [
            {'label': 'Classificação de Risco', 'url': reverse('saude_atendimento:classificacao_risco_list')},
        ]
        context['buscar_nome'] = self.request.GET.get('buscar_nome', "")
        context['opcao_filtro'] = self.request.GET.get('opcao_filtro', "") if self.request.GET.get('opcao_filtro', "") else "paciente"

        return context

class ListaChamadaClassificacaoRiscoCreateView(CheckUserTypeMixin, LoginRequiredMixin, CreateView):

    def get(self, request, boletim_id, *args, **kwargs):
        boletim = get_object_or_404(BoletimPaciente, id=boletim_id)

        lista_de_chamada, created = ListaChamadaClassificacaoRisco.objects.get_or_create(
            boletim=boletim,
            defaults={
                'sala': self.request.user.get_unidade_login().sala,
                'unidade_saude': self.request.user.get_unidade_login().unidade,
                'profissional': self.request.user.profissional_set.first(),
            }
        )
       
        return redirect('saude_atendimento:classificacao_risco_list')
    
class ClassificacaoRiscoCreateView(CheckUserTypeMixin, LoginRequiredMixin, SuccessMessageMixin, SaudeCheckHasPermission, CreateView):
    model = ClassificacaoRisco
    template_name = 'saude_atendimento/urgencia/classificacao_risco_create_update.html'
    form_class = ClassificacaoRiscoCriarForm
    required_permissions = [settings.DESENVOLVEDOR, settings.ENFERMEIRO, settings.TECNICO_ENFERMAGEM, settings.ADMINISTRADO, settings.MEDICO]
    success_url = reverse_lazy('saude_atendimento:classificacao_risco_list')
    success_message = 'Seus dados foram cadastrado conforme preencimento do formulário.'

    def dispatch(self, request, *args, **kwargs):
        
        if not request.user.is_authenticated or request.user.is_anonymous:
            response = super().dispatch(request, *args, **kwargs)
            return response

        if self.request.GET.get('paciente'):
            return super().dispatch(request, *args, **kwargs)
            
        messages.warning(self.request, 'Por favor, você precisa informar o paciente.')
        return redirect(reverse('saude_atendimento:classificacao_risco_list'))
    
    def form_valid(self, form):
        
        object = form.cleaned_data
        object['profissional'] = self.request.user.profissional_set.first()
        enfermeiro = self.request.user.profissional_set.first()
        acao = self.request.POST.get("acao", "")

        if object['tipo_fluxo'] == 1:
            object['tipo_atendimento'] = 'ENF'
        else:
            object['tipo_atendimento'] = 'BAU'

        classificacao = ClassificacaoRisco.objects.create(**object)
        classificacao = ClassificacaoRisco.objects.get(pk=classificacao.pk)

        lista_chamada_classificacao = ListaChamadaClassificacaoRisco.objects.filter(boletim=self.kwargs.get('pk'), situacao=ListaChamadaClassificacaoRisco.EM_ATENDIMENTO).first()

        if lista_chamada_classificacao:
            lista_chamada_classificacao.situacao = ListaChamadaClassificacaoRisco.CLASSIFICADO
            lista_chamada_classificacao.save()

        if acao == "urgencia":
            
            if object['tipo_fluxo'] == 1:
                chamado = ListaChamadoAdministracaoProcedimento.objects.create(
                    classificacao_risco=classificacao,
                    situacao=ListaChamadoAdministracaoProcedimento.DESIGNADO,
                    unidade_saude=object['profissional'].unidadelogin.unidade,
                    enfermeiro=enfermeiro,
                    contagem=1
                )

                paciente_pk = chamado.classificacao_risco.paciente.pk if chamado.classificacao_risco.paciente else None

                return redirect('saude_enfermagem:administracao_procedimento_create', pk=chamado.pk)

            return redirect('saude_atendimento:classificacao_risco_list')
        
        elif acao == "finalizar":
            print("Entrou no bloco SALVAR2")

            if object['tipo_fluxo'] == 1:
                chamado = ListaChamadoAdministracaoProcedimento.objects.create(
                    classificacao_risco=classificacao,
                    situacao=ListaChamadoAdministracaoProcedimento.CONCLUIDO,
                    unidade_saude=object['profissional'].unidadelogin.unidade,
                    enfermeiro=enfermeiro,
                    contagem=1
                )
                paciente_pk = chamado.classificacao_risco.paciente.pk if chamado.classificacao_risco.paciente else none
                paciente_instance = Paciente.objects.get(pk=paciente_pk) if paciente_pk else None

                receita = ReceitaAdministracaoProcedimento.objects.create(
                    paciente=paciente_instance,
                    enfermeiro=enfermeiro,
                    lista_chamada_solicitacao=chamado,
                    unidade_saude=object['profissional'].unidadelogin.unidade,
                    arquivo=None,
                    foto_receita=None
                )

                procedimento_instance = Procedimento.objects.get(pk=UUID('371b9b17-3756-4aef-ab28-1aead2e79fa8'))
                admin_proc = AdministracaoProcedimento.objects.create(
                    receita_procedimento=receita,
                    procedimento=procedimento_instance,
                    quantidade=1,
                    justificativa = 'finalização do procedimento eletivo feito pelo enfermeiro direto da triagem',
                    observacao = 'finalização do procedimento eletivo feito pelo enfermeiro direto da triagem'
                )

                situacao = SituacaoAdministracaoProcedimento.objects.create(
                    administracao_procedimento=admin_proc,
                    enfermeiro=enfermeiro,
                    data_hora_execucao=timezone.now(),
                    situacao=SituacaoAdministracaoProcedimento.REALIZADO,
                    sequencial=1,
                    justificativa = 'finalização do procedimento eletivo feito pelo enfermeiro direto da triagem'
                )

                boletim = chamado.classificacao_risco.boletim 
                boletim.situacao = 10
                boletim.save()

        return redirect('saude_atendimento:classificacao_risco_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_atual'] = timezone.now()
        context['crumbs'] = [
            {'label': 'Classificação de Risco', 'url': reverse('saude_atendimento:classificacao_risco_list')},
            {'label': 'Criação da Classificação de Risco', 'url': reverse('saude_atendimento:classificacao_risco_list')},
        ]
        context['tipo_classificacao_risco'] = TipoClassificacaoRisco.objects.filter(unidade_saude=self.request.user.get_unidade_login().unidade, situacao=TipoClassificacaoRisco.ATIVO)
        context['boletim'] = BoletimPaciente.objects.get(pk=self.kwargs.get('pk'))
        context['ultimo_atendimento'] = BoletimPaciente.objects.filter(paciente=self.request.GET.get('paciente')).exclude(situacao__in=[BoletimPaciente.EM_ABERTO, BoletimPaciente.EM_ANDAMENTO]).order_by('-created_at').first()

        lista_chamada_classificacao = ListaChamadaClassificacaoRisco.objects.filter(boletim__pk=self.kwargs.get('pk'), situacao=ListaChamadaClassificacaoRisco.CHAMADO).first()

        if lista_chamada_classificacao:
            lista_chamada_classificacao.situacao = ListaChamadaClassificacaoRisco.EM_ATENDIMENTO
            lista_chamada_classificacao.save()
        
        if self.request.GET.get('paciente'):
            context['object_paciente'] = Paciente.objects.get(pk=self.request.GET.get('paciente'))
        
        context['lista_chamada_classificacao'] = ListaChamadaClassificacaoRisco.objects.filter(boletim__pk=self.kwargs.get('pk')).first()
        
        return context
    
class ClassificacaoRiscoUpdateView(CheckUserTypeMixin, LoginRequiredMixin, SuccessMessageMixin, SaudeCheckHasPermission, UpdateView):
    model = ClassificacaoRisco
    template_name = 'saude_atendimento/urgencia/classificacao_risco_create_update.html'
    form_class = ClassificacaoRiscoAtualizarForm
    required_permissions = [settings.DESENVOLVEDOR, settings.ENFERMEIRO, settings.TECNICO_ENFERMAGEM, settings.ADMINISTRADO, settings.MEDICO]
    success_url = reverse_lazy('saude_atendimento:classificacao_risco_list')
    success_message = 'Seus dados foram atualizados conforme preencimento do formulário.'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if not request.user.is_authenticated or request.user.is_anonymous:
            return response
        
        # if ListaChamada.objects.filter(classificacao_risco__pk=kwargs.get('pk')).exists():
        #     messages.warning(self.request, 'Já existe uma chamada para classificacao de risco especificada.')
        #     return redirect(reverse('saude_atendimento:classificacao_risco_list'))

        if self.request.GET.get('paciente'):
            return super().dispatch(request, *args, **kwargs)
            
        messages.warning(self.request, 'Por favor, você precisa informar o paciente.')
        return redirect(reverse('saude_atendimento:classificacao_risco_list'))

    def form_valid(self, form):
        original_instance = self.get_object()
        profissional=Profissional.objects.get(user=self.request.user)

        # Desativar a instância original
        original_instance.status = ClassificacaoRisco.DESABILITADO
        original_instance.save()

        # Verificar se já existe uma nova instância ativa para evitar duplicação
        if not ClassificacaoRisco.objects.filter(paciente=original_instance.paciente, boletim=original_instance.boletim, status=ClassificacaoRisco.ATIVO).exists():
            new_instance = ClassificacaoRisco.objects.create(
                paciente=original_instance.paciente,
                profissional=profissional,
                boletim=original_instance.boletim,
                data_hora_avaliacao=timezone.now(),
                queixa_principal=form.cleaned_data.get('queixa_principal'),
                peso=form.cleaned_data.get('peso'),
                altura=form.cleaned_data.get('altura'),
                escala_dor=form.cleaned_data.get('escala_dor'),
                setor=original_instance.setor,
                status=ClassificacaoRisco.ATIVO,
                reclassificacao=True,
                estado_geral=form.cleaned_data.get('estado_geral'),
                observacao=form.cleaned_data.get('observacao'),
                presao_arterial=form.cleaned_data.get('presao_arterial'),
                frequencia_cardiaca=form.cleaned_data.get('frequencia_cardiaca'),
                frequencia_respiratoria=form.cleaned_data.get('frequencia_respiratoria'),
                temperatura=form.cleaned_data.get('temperatura'),
                spo2=form.cleaned_data.get('spo2'),
                hgt=form.cleaned_data.get('hgt'),
                tipo_classificacao_risco=form.cleaned_data.get('tipo_classificacao_risco'),
                tipo_atendimento=original_instance.tipo_atendimento,
                numero_atendimento=original_instance.numero_atendimento,
            )

            lista_chamada = ListaChamada.objects.filter(classificacao_risco__boletim=new_instance.boletim).first()
            if lista_chamada:
                lista_chamada.situacao = None
                lista_chamada.contagem = 0
                lista_chamada.save(skip_hooks=True)

            messages.success(self.request, 'Reclassificação atualizada com sucesso.')
        else:
            messages.warning(self.request, 'Já existe uma classificação de risco ativa para este paciente e boletim.')

        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_atual'] = timezone.now()
        boletim = self.get_object().boletim
        
        context['tipo_classificacao_risco'] = TipoClassificacaoRisco.objects.filter(unidade_saude=self.request.user.get_unidade_login().unidade)
        context['lista_chamada_classificacao'] = ListaChamadaClassificacaoRisco.objects.filter(boletim__id=boletim.id).first()

        context['crumbs'] = [
            {'label': 'Classificação de Risco', 'url': reverse('saude_atendimento:classificacao_risco_list')},
            {'label': 'Editar Classificação de Risco', 'url': reverse('saude_atendimento:classificacao_risco_list')},
        ]
        context['boletim'] = boletim
        
        if self.request.GET.get('paciente'):

            context['object_paciente'] = Paciente.objects.get(pk=self.request.GET.get('paciente'))
        
        return context
    
class RelatorioClassificacaoPacientePDFView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, TemplateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ENFERMEIRO, settings.TECNICO_ENFERMAGEM, settings.ADMINISTRADO]
    template_name = "exportacao/classificacao_risco_pdf.html"

    def get_context_data(self, **kwargs):
        context = super(RelatorioClassificacaoPacientePDFView, self).get_context_data(**kwargs)

        data_hora_atual = datetime.now()

        context['data_impressao'] = data_hora_atual.strftime("%d/%m/%d %H:%M")
        context['title_relatorio'] = 'Registro da Classificação de Risco'
        context['classificacao_risco'] = ClassificacaoRisco.objects.get(pk=kwargs.get('pk'))
        context['unidade_saude'] = self.request.user.get_unidade_login().unidade
        
        return context
    
class ListaChamadaCreateView(CheckUserTypeMixin, LoginRequiredMixin, CreateView):

    def get(self, request, id_paciente, id_boletim, *args, **kwargs):
        paciente = get_object_or_404(Paciente, id=id_paciente)
        boletim_id = get_object_or_404(BoletimPaciente, id=id_boletim)
        classificacao_risco = ClassificacaoRisco.objects.filter(paciente=paciente, boletim=boletim_id, status=ClassificacaoRisco.ATIVO).first()

        lista_chamada = ListaChamada.objects.filter(classificacao_risco__boletim=boletim_id).first()
        if not lista_chamada:
            lista_de_chamados, created = ListaChamada.objects.get_or_create(
                paciente=paciente,
                classificacao_risco=classificacao_risco,
                defaults={
                    'sala': self.request.user.get_unidade_login().sala,
                    'unidade_saude': self.request.user.get_unidade_login().unidade,
                    'medico': self.request.user.profissional_set.first(),
                }
            )
            if not created:
                lista_de_chamados.situacao = ListaChamada.RETORNO
                lista_de_chamados.contagem = 1
                lista_de_chamados.save()

        elif lista_chamada.situacao == ListaChamada.LISTA_RETORNO:
            lista_chamada.situacao = ListaChamada.RETORNO
            lista_chamada.contagem = 1
            lista_chamada.save()
        else:
            lista_chamada.classificacao_risco = classificacao_risco
            lista_chamada.situacao = ListaChamada.EM_ESPERA
            lista_chamada.contagem = 1
            lista_chamada.save()
       
        return redirect('saude_atendimento:atendimento_medico_list')
    
class AtendimentoMedicoListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    model = ClassificacaoRisco
    required_permissions = [settings.DESENVOLVEDOR, settings.MEDICO, settings.ADMINISTRADO]
    template_name = "saude_atendimento/urgencia/atendimento_medico_list.html"

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if not request.user.is_authenticated or request.user.is_anonymous:
            return response
        
        if self.request.user.tipo_usuario == 'desenvolvedor' or self.request.user.tipo_usuario == 'administrador':
            if not self.request.user.get_unidade_login().sala:
                messages.warning(request, 'Você precisa selecionar uma sala antes de iniciar os atendimentos!')
                params = {'setor': '1'}
                url = f"{reverse('saude:selecao_salas_list')}?{urlencode(params)}"

                return redirect(url)
            
            elif self.request.user.get_unidade_login().sala.unidade_setor.tipo != UnidadeSetor.URGENCIA :
                messages.warning(request, 'Você precisa selecionar uma sala da urgência antes de iniciar os atendimentos!')
                params = {'setor': '1'}
                url = f"{reverse('saude:selecao_salas_list')}?{urlencode(params)}"

                return redirect(url)
            
        if self.request.user.tipo_usuario == 'medico':
            if not request.user.get_unidade_login().sala:
                messages.warning(request, 'Selecione uma sala antes de iniciar os atendimentos!')
                params = {'setor': '1'}
                url = f"{reverse('saude:selecao_salas_list')}?{urlencode(params)}"

                return redirect(url)
            
            elif self.request.user.get_unidade_login().sala.unidade_setor.tipo != UnidadeSetor.URGENCIA :
                messages.warning(request, 'Você precisa selecionar uma sala da urgência antes de iniciar os atendimentos!')
                params = {'setor': '1'}
                url = f"{reverse('saude:selecao_salas_list')}?{urlencode(params)}"

                return redirect(url)
            
        return super(AtendimentoMedicoListView, self).dispatch(request, *args, **kwargs)
        
    def get_queryset(self):
        queryset = super().get_queryset().filter(boletim__unidade_saude=self.request.user.get_unidade_login().unidade)

        if self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "paciente":
            queryset = queryset.filter(paciente__nome_paciente__icontains=self.request.GET.get('buscar_nome'))
            
        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "cpf":
            queryset = queryset.filter(paciente__cpf=self.request.GET.get('buscar_nome'))

        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "rg":
            queryset = queryset.filter(paciente__rg=self.request.GET.get('buscar_nome'))

        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "sus":
            queryset = queryset.filter(paciente__cartao_sus=self.request.GET.get('buscar_nome'))
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        context['esperando_chamadas'] = self.get_queryset().filter(
            Q(tipo_atendimento='BAU') &
            Q(tipo_fluxo=ClassificacaoRisco.FLUXO_URGENCIA) &
            Q(status=ClassificacaoRisco.ATIVO),
            Q(
                Q(setor=ClassificacaoRisco.TRIAGEM, classificacao_risco_lista_chamada_set__isnull=True, boletim__situacao=BoletimPaciente.EM_ABERTO)
            ) | 
            Q(classificacao_risco_lista_chamada_set__situacao=ListaChamada.LISTA_RETORNO)
        ).order_by(
            Case(
                When(tipo_classificacao_risco__tipo=4, then=Value(0)),
                When(tipo_classificacao_risco__tipo=3, then=Value(1)),
                When(tipo_classificacao_risco__tipo=2, then=Value(2)),
                When(tipo_classificacao_risco__tipo=1, then=Value(3)),
                When(tipo_classificacao_risco__tipo=0, then=Value(4)),
                default=Value(4),
                output_field=IntegerField(),
            ),
            'paciente__data_nascimento'
        ).distinct()

        context['lista_chamadas'] = self.get_queryset().filter(
            status=ClassificacaoRisco.ATIVO,
            classificacao_risco_lista_chamada_set__situacao__in=[
                ListaChamada.EM_ESPERA, 
                # ListaChamada.EM_ATENDIMENTO_RETORNO,
                ListaChamada.RETORNO
            ],
            classificacao_risco_lista_chamada_set__sala=self.request.user.get_unidade_login().sala,
        ).order_by(
            Case(
                When(classificacao_risco_lista_chamada_set__classificacao_risco__tipo_classificacao_risco__tipo=4, then=Value(0)),
                When(classificacao_risco_lista_chamada_set__classificacao_risco__tipo_classificacao_risco__tipo=3, then=Value(1)),
                When(classificacao_risco_lista_chamada_set__classificacao_risco__tipo_classificacao_risco__tipo=2, then=Value(2)),
                When(classificacao_risco_lista_chamada_set__classificacao_risco__tipo_classificacao_risco__tipo=1, then=Value(3)),
                When(classificacao_risco_lista_chamada_set__classificacao_risco__tipo_classificacao_risco__tipo=0, then=Value(4)),
                default=Value(4),
                output_field=IntegerField(),
            ),
            'paciente__data_nascimento'
        ).distinct()

        context['data_atual'] = timezone.now()
        context['crumbs'] = [{'label': 'Atendimento Médico', 'url': reverse('saude_atendimento:atendimento_medico_list')},]
        context['buscar_nome'] = self.request.GET.get('buscar_nome', "")
        context['opcao_filtro'] = self.request.GET.get('opcao_filtro', "") if self.request.GET.get('opcao_filtro', "") else "paciente"

        return context
    
class AtendimentoMedicoDetailView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, DetailView):
    model = ListaChamada
    required_permissions = [settings.DESENVOLVEDOR, settings.MEDICO, settings.ADMINISTRADO]
    template_name = 'saude_atendimento/urgencia/atendimento_medico_detail.html'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if not request.user.is_authenticated or request.user.is_anonymous:
            return response
        
        if self.get_object().situacao == ListaChamada.LISTA_RETORNO:
            return redirect(reverse('saude_atendimento:atendimento_medico_list'))
        
        return super().dispatch(request, *args, **kwargs)
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        atendimento, created = AtendimentoMedico.objects.get_or_create(
            lista_chamada=self.object,
            defaults={
                'paciente': self.object.paciente,
                'unidade_saude': self.request.user.get_unidade_login().unidade,
            }
        )
        if atendimento.lista_chamada.situacao == ListaChamada.EM_ESPERA:
            classificacao_risco = ClassificacaoRisco.objects.filter(boletim=self.object.classificacao_risco.boletim)
            atendimento.classificacao_risco.add(*classificacao_risco)
            self.object.situacao = ListaChamada.EM_ATENDIMENTO
            self.object.save()

        if atendimento and self.request.user.profissional_set.first() not in atendimento.profissionais.all():
            atendimento.profissionais.add(self.request.user.profissional_set.first())
            atendimento.save()

        if self.object.situacao == ListaChamada.RETORNO:
            self.object.situacao = ListaChamada.EM_ATENDIMENTO_RETORNO
            self.object.save()

        context['crumbs'] = [
            {'label': 'Atendimento Médico Listagem', 'url': reverse('saude_atendimento:atendimento_medico_list')},
            {'label': 'Atendimento Médico', 'url': '#'},
        ]
        context['data_atual'] = timezone.now()
        context['ultimo_atendimento'] = BoletimPaciente.objects.filter(paciente=self.object.paciente).exclude(
            situacao__in=[BoletimPaciente.EM_ABERTO, BoletimPaciente.EM_ANDAMENTO]).order_by('-created_at').first()
        
        context['historico_chamado'] = HistoricoEsperaAtendimento.objects.filter(lista_chamada=self.get_object()).order_by('-created_at').first()
      
        context['profissional_pk'] = self.request.user.profissional_set.first().pk
        context['unidade_saude_session_id'] = self.request.user.get_unidade_login().unidade.id

        return context

class PacientesAguardandoAtendimentoListView(CheckUserTypeMixin, LoginRequiredMixin, ListView):
    model = ListaChamada
    context_object_name = 'pacientes'
    # required_permissions = [settings.DESENVOLVEDOR, settings.RECEPCIONISTA, settings.ADMINISTRADO]
    template_name = 'saude_atendimento/urgencia/pacientes_aguardando_atendimento_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            unidade_saude=self.request.user.get_unidade_login().unidade,
        ).order_by('paciente__nome_paciente')

        if self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "paciente":
            queryset = queryset.filter(paciente__nome_paciente__icontains=self.request.GET.get('buscar_nome'))
            
        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "cpf":
            queryset = queryset.filter(paciente__cpf=self.request.GET.get('buscar_nome'))

        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "rg":
            queryset = queryset.filter(paciente__rg=self.request.GET.get('buscar_nome'))

        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "sus":
            queryset = queryset.filter(paciente__cartao_sus=self.request.GET.get('buscar_nome'))
      
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        listagem_chamadas = self.get_queryset().order_by(
            Case(
                When(classificacao_risco__tipo_classificacao_risco=4, then=Value(0)),
                When(classificacao_risco__tipo_classificacao_risco=3, then=Value(1)),
                When(classificacao_risco__tipo_classificacao_risco=2, then=Value(2)),
                When(classificacao_risco__tipo_classificacao_risco=1, then=Value(3)),
                When(classificacao_risco__tipo_classificacao_risco=0, then=Value(4)),
                default=Value(4),
                output_field=IntegerField(),
            )
        )
        
        context["atendimentos_aguardando"] = listagem_chamadas.filter(situacao=ListaChamada.EM_ESPERA)
        context["sendo_atendidos"] = listagem_chamadas.filter(situacao=ListaChamada.EM_ATENDIMENTO)
        context['crumbs'] = [
            {'label': 'Pacientes Aguardando Atendimento', 'url': reverse('saude_atendimento:pacientes_aguardando_atendimento_list')},
        ]
        context['buscar_nome'] = self.request.GET.get('buscar_nome', "")
        context['opcao_filtro'] = self.request.GET.get('opcao_filtro', "") if self.request.GET.get('opcao_filtro', "") else "paciente"

        return context

class RelatorioPacienteAtendimentoPDFView(CheckUserTypeMixin, LoginRequiredMixin, TemplateView):
    template_name = "exportacao/paciente_atendimento_pdf.html"

    def get_context_data(self, **kwargs):
        context = super(RelatorioPacienteAtendimentoPDFView, self).get_context_data(**kwargs)

        data_hora_atual = datetime.now()

        context['data_impressao'] = data_hora_atual.strftime("%d/%m/%d %H:%M")
        context['title_relatorio'] = 'Ficha de Atendimento Médico'
        context['atendimento_medico'] = AtendimentoMedico.objects.get(pk=kwargs.get('pk'))

        return context
    
class TipoAltaHospitalarListView(CheckUserTypeMixin, LoginRequiredMixin, ListView):
    model = TipoAltaHospitalar
    context_object_name = 'tiposdealtahospitalar'
    template_name = 'saude_atendimento/urgencia/tipo_de_alta_hospitalar.html'
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

        for situacao in TipoAltaHospitalar.SITUACOES_CHOICES:
            situacoes.append(situacao[1])

        context['situacoes'] = situacoes

        context['crumbs'] = [
            {'label': 'Listagem de Tipos de Alta Hospitalar', 'url': reverse('saude_atendimento:tipoaltahospitalar_list')}
        ]

        return context

class TipoAltaHospitalarCreateView(CheckUserTypeMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = TipoAltaHospitalar
    template_name = 'saude_atendimento/urgencia/tipo_de_alta_hospitalar_create_update_form.html'
    form_class = TipoAltaHospitalarForm
    success_url = reverse_lazy('saude_atendimento:tipoaltahospitalar_list')
    success_message = 'Seus dados foram cadastrado conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['crumbs'] = [
            {'label': 'Listagem de Tipos de Alta Hospitalar', 'url': reverse('saude_atendimento:tipoaltahospitalar_list')},
            {'label': 'Cadastro de Tipo de Alta Hospitalar', 'url': reverse('saude_atendimento:tipoaltahospitalar_add')}
        ]

        return context

class TipoAltaHospitalarUpdateView(CheckUserTypeMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TipoAltaHospitalar
    template_name = 'saude_atendimento/urgencia/tipo_de_alta_hospitalar_create_update_form.html'
    form_class = TipoAltaHospitalarForm
    success_url = reverse_lazy('saude_atendimento:tipoaltahospitalar_list')
    success_message = 'Seus dados foram alterados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['crumbs'] = [
            {'label': 'Listagem de Tipos de Alta Hospitalar', 'url': reverse('saude_atendimento:tipoaltahospitalar_list')},
            {'label': 'Editar dados do tipo de alta hospitalar', 'url': reverse('saude_atendimento:tipoaltahospitalar_update', kwargs={'pk': self.object.pk})}
        ]

        return context

class TipoAltaHospitalarDeleteView(CheckUserTypeMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TipoAltaHospitalar
    template_name = "saude_atendimento/urgencia/tipo_de_alta_hospitalar.html"
    success_url = reverse_lazy('saude_atendimento:tipoaltahospitalar_list')
    success_message = 'Seus dados foram deletados conforme solicitado.'
    
class EncaminhamentoListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    required_permissions = [settings.DESENVOLVEDOR, settings.RECEPCIONISTA, settings.ENFERMEIRO,  settings.MEDICO, settings.ADMINISTRADO, settings.ADMINISTRADO]
    model = BoletimPaciente
    context_object_name = "boletimPaciente"
    template_name = "saude_atendimento/urgencia/encaminhamento_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            unidade_saude=self.request.user.get_unidade_login().unidade, situacao=BoletimPaciente.EM_ABERTO
        ).order_by('paciente__nome_paciente')

        if self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "paciente":
            queryset = queryset.filter(paciente__nome_paciente__icontains=self.request.GET.get('buscar_nome'))
            
        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "cpf":
            queryset = queryset.filter(paciente__cpf=self.request.GET.get('buscar_nome'))

        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "rg":
            queryset = queryset.filter(paciente__rg=self.request.GET.get('buscar_nome'))

        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "sus":
            queryset = queryset.filter(paciente__cartao_sus=self.request.GET.get('buscar_nome'))
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        url = reverse('saude_atendimento:encaminhamento_list')

        context['crumbs'] = [
            {'label': 'Encaminhamento', 'url': url},
        ]

        context['buscar_nome'] = self.request.GET.get('buscar_nome', "")
        context['opcao_filtro'] = self.request.GET.get('opcao_filtro', "") if self.request.GET.get('opcao_filtro', "") else "paciente"

        return context
    
class ConcessaoDeAltaListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    required_permissions = [settings.DESENVOLVEDOR, settings.MEDICO, settings.ADMINISTRADO]
    model = ListaChamada
    context_object_name = "em_atendimento"
    template_name = "saude_atendimento/urgencia/concessao_alta_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            unidade_saude=self.request.user.get_unidade_login().unidade,
            situacao__in=[ListaChamada.EM_ESPERA, ListaChamada.EM_ATENDIMENTO, ListaChamada.EM_PROCEDIMENTO, ListaChamada.RETORNO, ListaChamada.EM_ATENDIMENTO_RETORNO]
        ).order_by('paciente__nome_paciente')

        if self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "paciente":
            queryset = queryset.filter(paciente__nome_paciente__icontains=self.request.GET.get('buscar_nome'))
            
        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "cpf":
            queryset = queryset.filter(paciente__cpf=self.request.GET.get('buscar_nome'))

        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "rg":
            queryset = queryset.filter(paciente__rg=self.request.GET.get('buscar_nome'))

        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "sus":
            queryset = queryset.filter(paciente__cartao_sus=self.request.GET.get('buscar_nome'))
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        url = reverse('saude_atendimento:concessao_alta_list')

        context['crumbs'] = [
            {'label': 'Alta Hospitalar', 'url': url},
        ]

        context['buscar_nome'] = self.request.GET.get('buscar_nome', "")
        context['opcao_filtro'] = self.request.GET.get('opcao_filtro', "") if self.request.GET.get('opcao_filtro', "") else "paciente"

        return context

class AtendimentosEmAbertoListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    model = AtendimentoMedico
    required_permissions = [settings.DESENVOLVEDOR, settings.MEDICO, settings.ADMINISTRADO]
    template_name = "saude_atendimento/urgencia/atendimento_em_aberto_list.html"

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            lista_chamada__sala=self.request.user.get_unidade_login().sala,
            unidade_saude=self.request.user.get_unidade_login().unidade,
            lista_chamada__situacao__in=[ListaChamada.EM_ATENDIMENTO, ListaChamada.EM_PROCEDIMENTO, ListaChamada.RETORNO, ListaChamada.EM_ATENDIMENTO_RETORNO, ListaChamada.ATENDIMENTO_REABERTO]
        )

        if self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "paciente":
            queryset = queryset.filter(paciente__nome_paciente__icontains=self.request.GET.get('buscar_nome'))
            
        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "cpf":
            queryset = queryset.filter(paciente__cpf=self.request.GET.get('buscar_nome'))

        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "rg":
            queryset = queryset.filter(paciente__rg=self.request.GET.get('buscar_nome'))

        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "sus":
            queryset = queryset.filter(paciente__cartao_sus=self.request.GET.get('buscar_nome'))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buscar_nome'] = self.request.GET.get('buscar_nome', "")
        context['opcao_filtro'] = self.request.GET.get('opcao_filtro', "") if self.request.GET.get('opcao_filtro', "") else "paciente"
        
        return context

class AtendimentoAtestadoListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    model = AtestadoAtendimento
    context_object_name = "atestado"
    template_name = "saude_atendimento/urgencia/atendimento_atestado_medico_list.html"
    required_permissions = [settings.DESENVOLVEDOR, settings.MEDICO, settings.ADMINISTRADO]

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset().filter(
            atendimento__paciente__pk=self.request.GET.get('pk')).order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_atual'] = timezone.now()
        context['paciente_pk'] = self.request.GET.get('pk')
        context['object_paciente'] = Paciente.objects.get(pk=self.request.GET.get('pk'))
        context['lista_chamada'] = ListaChamada.objects.filter(pk=self.request.GET.get('lista')).order_by('-created_at').first()
        return context

class AtendimentoAtestadoCreateView(CheckUserTypeMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AtestadoAtendimento
    template_name = 'saude_atendimento/urgencia/atendimento_atestado_medico_create.html'
    form_class = AtestadoAtendimentoForm
    success_message = 'Seus dados foram cadastrado conforme preenchimento no formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_atual'] = timezone.now()
        context['paciente'] =  Paciente.objects.get(pk=self.request.GET.get('pk'))
        context['atendimento'] = AtendimentoMedico.objects.filter(lista_chamada=self.request.GET.get('lista')).order_by('-created_at').first()
        context['diagnostico'] = DiagnosticoAtendimento.objects.filter(atendimento__lista_chamada__pk=self.request.GET.get('lista'))
        return context

    def form_valid(self, form):
        profissional=Profissional.objects.get(user=self.request.user)

        self.object = form.save(commit=False)
        self.object.profissional=profissional
        self.object.save()

        paciente_pk = self.request.GET.get('pk')
        lista = ListaChamada.objects.get(pk=self.request.GET.get('lista'))

        url = reverse('saude_atendimento:atendimento_atestado_list')
        url_com_parametro = f"{url}?pk={paciente_pk}&lista={lista.id}&impressao={self.object.pk}"

        return HttpResponseRedirect(url_com_parametro)
    
class AtendimentoAtestadoPdfView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, DetailView):
    model = AtestadoAtendimento
    context_object_name = "atestado"
    template_name = "exportacao/atendimento_atestado_pdf.html"
    required_permissions = [settings.DESENVOLVEDOR, settings.MEDICO, settings.ADMINISTRADO]

    def get_context_data(self, **kwargs):
        context = super(AtendimentoAtestadoPdfView, self).get_context_data(**kwargs)

        context['data_atual'] = timezone.now()
        context['title_relatorio'] = 'Atestado Médico'
        context['unidade_saude'] = self.request.user.get_unidade_login().unidade

        return context
    
class AtendimentoFichaReferenciaListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    model = FichaReferenciaAtendimento
    template_name = "saude_atendimento/urgencia/atendimento_ficha_referencia_list.html"
    required_permissions = [settings.DESENVOLVEDOR, settings.MEDICO, settings.ADMINISTRADO]

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset().filter(
            atendimento__paciente__pk=self.request.GET.get('pk')).order_by('-created_at')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_atual'] = timezone.now()
        context['object_paciente'] = Paciente.objects.get(pk=self.request.GET.get('pk'))
        
        return context
    
class AtendimentoFichaReferenciaCreateView(CheckUserTypeMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = FichaReferenciaAtendimento
    template_name = 'saude_atendimento/urgencia/atendimento_ficha_referencia_create.html'
    success_message = 'Seus dados foram cadastrado conforme preenchimento no formulário.'
    form_class = FichaReferenciaAtendimentoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_atual'] = timezone.now()
        context['atendimento'] = AtendimentoMedico.objects.filter(
            Q(pk=self.kwargs.get('pk')) & 
            (Q(lista_chamada__situacao=ListaChamada.EM_ATENDIMENTO) | 
            Q(lista_chamada__situacao=ListaChamada.RETORNO))
        ).order_by('-created_at').first()
        return context
    
    def form_valid(self, form):
        object = form.save(commit=False)
        checkbox_exames = form.cleaned_data['exames']
        checkbox_tratamentos = form.cleaned_data['tratamentos']
        checkbox_diagnosticos = form.cleaned_data['diagnosticos']

        object.profissional = self.request.user.profissional_set.first()
        object.save()
        
        atendimento = AtendimentoMedico.objects.get(pk=object.atendimento.pk)
        
        if checkbox_exames:
            exames = ExameAtendimento.objects.filter(pk__in=atendimento.atendimento_exame_atendimento_set.all().values('id'))
            object.exames.add(*exames)
        if checkbox_tratamentos:
            medicacoes = MedicacaoAtendimento.objects.filter(pk__in=atendimento.medicacaoatendimento_set.all().values('id'))
            object.medicacoes.add(*medicacoes)
        if checkbox_diagnosticos:
            diagnosticos = DiagnosticoAtendimento.objects.filter(pk__in=atendimento.atendimento_diagnostico_atendimento_set.all().values('id'))
            object.diagnosticos.add(*diagnosticos)
        object.save()

        url = reverse('saude_atendimento:atendimento_ficha_list')
        url_com_parametro = f"{url}?pk={object.atendimento.paciente.pk}&impressao={object.pk}"

        return HttpResponseRedirect(url_com_parametro)

class AtendimentoFichaReferenciaPdfView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, DetailView):
    model = FichaReferenciaAtendimento
    template_name = "exportacao/atendimento_ficha_referencia_pdf.html"
    required_permissions = [settings.DESENVOLVEDOR, settings.MEDICO, settings.ADMINISTRADO]

    def get_context_data(self, **kwargs):
        context = super(AtendimentoFichaReferenciaPdfView, self).get_context_data(**kwargs)

        context['data_atual'] = timezone.now()
        context['title_relatorio'] = 'Ficha de referência médica'
        context['data_impressao'] = timezone.now()
        context['unidade_saude'] = self.request.user.get_unidade_login().unidade

        return context

class DeclaracaoAcompanhantePdfView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, TemplateView):
    template_name = "exportacao/declaracao_acompanhante_paciente.html"
    required_permissions = [settings.DESENVOLVEDOR, settings.MEDICO, settings.ADMINISTRADO]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_atual'] = timezone.now()
        context['title_relatorio'] = 'Declaração de Acompanhante do Paciente'
        context['atendimento'] = AtendimentoMedico.objects.filter(paciente__pk=kwargs.get('pk')).first()
        context['unidade_saude'] = self.request.user.get_unidade_login().unidade
        
        return context
    
class DeclaracaoConsultaExamePdfView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, TemplateView):
    template_name = "exportacao/declaracao_consulta_exame_pdf.html"
    required_permissions = [settings.DESENVOLVEDOR, settings.MEDICO, settings.ADMINISTRADO]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_atual'] = timezone.now()
        context['title_relatorio'] = 'Declaração de Comparecimento Consulta/Exames'
        context['atendimento'] = AtendimentoMedico.objects.filter(paciente__pk=kwargs.get('pk')).first()
        context['unidade_saude'] = self.request.user.get_unidade_login().unidade

        return context
    
class ReceitaPosteriorImediataPdfView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, TemplateView):
    template_name = "exportacao/receita_posterior_imediata.html"
    required_permissions = [settings.DESENVOLVEDOR, settings.MEDICO, settings.ADMINISTRADO]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('tipo') == 'posterior':
            context['receitas'] = MedicacaoAtendimento.objects.filter(atendimento__lista_chamada__pk=kwargs.get('pk'), aplicacao=MedicacaoAtendimento.POSTERIOR, medicamento_controlado=False)
            context['tipo'] = 'Posterior'

        elif self.request.GET.get('tipo') == 'controlada':
            context['receitas'] = MedicacaoAtendimento.objects.filter(atendimento__lista_chamada__pk=kwargs.get('pk'), medicamento_controlado=True)
            context['tipo'] = 'Controlada'
            context['title_relatorio'] = 'RECEITUÁRIO DE CONTROLE ESPECIAL'
            context['range'] = range(2)
        
        else:
            context['receitas'] = MedicacaoAtendimento.objects.filter(atendimento__lista_chamada__pk=kwargs.get('pk'), aplicacao=MedicacaoAtendimento.IMEDIATA)
            context['tipo'] = 'Imediata'

        context['data_impressao'] = timezone.now()
        
        if 'title_relatorio' not in context:
            context['title_relatorio'] = 'Receita Médica' + ' ' + context['tipo']
        context['profissional'] = Profissional.objects.get(id=self.request.user.profissional_set.first().id)
        context['atendimento'] = AtendimentoMedico.objects.filter(lista_chamada__pk=kwargs.get('pk')).first()
        context['unidade_saude'] = self.request.user.get_unidade_login().unidade

        return context
    
class AtendimentoMedicacaoPosteriorPdfView(CheckUserTypeMixin, LoginRequiredMixin, TemplateView):
    template_name = "exportacao/atendimento_exames_pdf.html"
    required_permissions = [settings.DESENVOLVEDOR, settings.MEDICO, settings.ADMINISTRADO]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_atual'] = timezone.now()
        context['title_relatorio'] = 'teste'

        return context
    
class JustificativaProcedimentoAtendimentoCreateView(CheckUserTypeMixin, LoginRequiredMixin, CreateView):
    model = JustificativaProcedimentoAtendimento
    template_name = 'saude_atendimento/urgencia/justificativa_procedimento_atendimento_create_update.html'
    form_class = JustificativaProcedimentoCreateForm

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if not request.user.is_authenticated or request.user.is_anonymous:
            return response
        
        if self.request.GET.get('atendimento'):
            return super().dispatch(request, *args, **kwargs)
        
        return redirect(reverse('saude_atendimento:atendimento_medico_list'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        atendimento = get_object_or_404(AtendimentoMedico, pk=self.request.GET.get('atendimento'))

        procedimentos = ProcedimentoAtendimento.objects.filter(atendimento=atendimento.id)

        context['atendimento'] = atendimento
        context['procedimentos'] = procedimentos
        return context
    
    def form_valid(self, form):
        atendimento = get_object_or_404(AtendimentoMedico, pk=self.request.GET.get('atendimento'))
        profissional=Profissional.objects.get(user=self.request.user)
    
        procedimentos = ProcedimentoAtendimento.objects.filter(atendimento=atendimento.pk)

        self.object = form.save(commit=False)
        self.object.atendimento = atendimento
        self.object.profissional=profissional
        self.object.save()

        self.object.procedimentos.set(procedimentos)

        return HttpResponseRedirect(reverse('saude_atendimento:atendimento_medico_detail', kwargs={'pk': atendimento.lista_chamada.pk}))

class JustificativaProcedimentoAtendimentoUpdateView(CheckUserTypeMixin, LoginRequiredMixin, UpdateView):
    model = JustificativaProcedimentoAtendimento
    template_name = 'saude_atendimento/urgencia/justificativa_procedimento_atendimento_create_update.html'
    form_class = JustificativaProcedimentoUpdateForm

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if not request.user.is_authenticated or request.user.is_anonymous:
            return response
        
        if self.request.GET.get('atendimento'):
            return super().dispatch(request, *args, **kwargs)
        
        return redirect(reverse('saude_atendimento:atendimento_medico_list'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        atendimento = get_object_or_404(AtendimentoMedico, pk=self.request.GET.get('atendimento'))

        procedimentos = ProcedimentoAtendimento.objects.filter(atendimento=atendimento.id)

        context['atendimento'] = atendimento
        context['procedimentos'] = procedimentos
        return context
    
    def form_valid(self, form):
        atendimento = get_object_or_404(AtendimentoMedico, pk=self.request.GET.get('atendimento'))
        procedimentos = ProcedimentoAtendimento.objects.filter(atendimento=atendimento.pk)

        self.object = form.save(commit=False)
        self.object.save()

        self.object.procedimentos.set(procedimentos)

        return HttpResponseRedirect(reverse('saude_atendimento:atendimento_medico_detail', kwargs={'pk': atendimento.lista_chamada.pk}))
    
class RelatorioProcedimentoSolicitacaoPDFView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, DetailView):
    required_permissions = [settings.DESENVOLVEDOR, settings.RECEPCIONISTA, settings.ADMINISTRADO, settings.MEDICO]
    model = JustificativaProcedimentoAtendimento
    context_object_name = "justificativa"
    template_name = "exportacao/atendimento_procedimento_solicitacao.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_impressao'] = timezone.now()
        context['title_relatorio'] = 'INFORMAÇÕES DOS PROCEDIMENTOS SOLICITADOS'
        context['unidade_saude'] = self.request.user.get_unidade_login().unidade

        return context

class AtendimentoFinalizadoListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    required_permissions = [settings.DESENVOLVEDOR, settings.MEDICO, settings.ADMINISTRADO]
    model = AtendimentoMedico
    template_name = 'saude_atendimento/urgencia/atendimentos_finalizados_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(lista_chamada__situacao__in=[ListaChamada.ENCERRADO_ATENDIMENTO, ListaChamada.ENCERRADO_ALTA, ListaChamada.ENCERRADO_RECEPCAO, ListaChamada.ENCERRADO_SISTEMA]).order_by('-lista_chamada__classificacao_risco__numero_atendimento')
        dois_dias_atras = timezone.now() - timedelta(days=2)

        if self.request.user.tipo_usuario == Profissional.MEDICO:
            queryset = queryset.filter(created_at__gte=dois_dias_atras)

        if self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "paciente":
            queryset = queryset.filter(paciente__nome_paciente__icontains=self.request.GET.get('buscar_nome'))
            
        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "cpf":
            queryset = queryset.filter(paciente__cpf=self.request.GET.get('buscar_nome'))

        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "rg":
            queryset = queryset.filter(paciente__rg=self.request.GET.get('buscar_nome'))

        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "sus":
            queryset = queryset.filter(paciente__cartao_sus=self.request.GET.get('buscar_nome'))
      
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crumbs'] = [{'label': 'Listagem de Atendimentos', 'url': '#'},]
        context['buscar_nome'] = self.request.GET.get('buscar_nome', "")
        context['opcao_filtro'] = self.request.GET.get('opcao_filtro', "") if self.request.GET.get('opcao_filtro', "") else "paciente"

        return context