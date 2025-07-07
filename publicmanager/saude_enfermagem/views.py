import tempfile
# import weasyprint
from django.db.models import Q
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from urllib.parse import urlencode
from datetime import datetime as dt
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, Value, When, IntegerField
from django.views.generic import ListView, UpdateView, DetailView, TemplateView, View

from publicmanager.comum.utils import CheckUserTypeMixin
from publicmanager.dashboard.utils import SaudeCheckHasPermission
from publicmanager.saude.templatetags.saude_extras import tempo_medio_espera_data_hora

from publicmanager.saude_cadastro.models import UnidadeSetor, Profissional
from publicmanager.saude_atendimento.models import BoletimPaciente, ClassificacaoRisco
from publicmanager.saude_enfermagem.models import (
    ListaChamadaSolicitacaoAtendimento, SolicitacaoAtendimento, ListaChamadoAdministracaoMedicamento, ReceitaMedicamento,
    ListaChamadoAdministracaoProcedimento, ReceitaAdministracaoProcedimento
)

class ExamesLaboratoriaisListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    model = ListaChamadaSolicitacaoAtendimento
    required_permissions = [settings.DESENVOLVEDOR, settings.ENFERMEIRO, settings.TECNICO_ENFERMAGEM, settings.ADMINISTRADO]
    template_name = "saude_enfermagem/exames_laboratoriais_list.html"

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if not request.user.is_authenticated or request.user.is_anonymous:
            return response
        
        if self.request.user.tipo_usuario == 'desenvolvedor' or self.request.user.tipo_usuario == 'administrador':
            if not self.request.user.get_unidade_login().sala:
                messages.warning(request, 'Selecione um laboratório antes de iniciar os atendimentos!')
                params = {'setor': '7'}
                url = f"{reverse('saude:selecao_salas_list')}?{urlencode(params)}"

                return redirect(url)
            
            elif self.request.user.get_unidade_login().sala.unidade_setor.tipo != UnidadeSetor.LABORATORIO :
                messages.warning(request, 'Você precisa selecionar uma sala do laboratório antes de iniciar os atendimentos!')
                params = {'setor': '7'}
                url = f"{reverse('saude:selecao_salas_list')}?{urlencode(params)}"

                return redirect(url)
            
        if self.request.user.tipo_usuario == 'enfermeiro' or self.request.user.tipo_usuario == 'tecnico_enfermagem':
            if not request.user.get_unidade_login().sala:
                messages.warning(request, 'Selecione um laboratório antes de iniciar os atendimentos!')
                params = {'setor': '7'}
                url = f"{reverse('saude:selecao_salas_list')}?{urlencode(params)}"

                return redirect(url)
            
            elif self.request.user.get_unidade_login().sala.unidade_setor.tipo != UnidadeSetor.LABORATORIO :
                messages.warning(request, 'Você precisa selecionar uma sala do laboratório antes de iniciar os atendimentos!')
               
                params = {'setor': '7'}
                url = f"{reverse('saude:selecao_salas_list')}?{urlencode(params)}"

                return redirect(url)
            
        return super(ExamesLaboratoriaisListView, self).dispatch(request, *args, **kwargs)
             
    def get_queryset(self):
        queryset = super().get_queryset().filter(unidade_saude=self.request.user.get_unidade_login().unidade, tipo=ListaChamadaSolicitacaoAtendimento.EXAME_LABORATORIO)

        if self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "paciente":
            queryset = queryset.filter(atendimento__paciente__nome_paciente__icontains=self.request.GET.get('buscar_nome'))
            
        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "cpf":
            queryset = queryset.filter(atendimento__paciente__cpf=self.request.GET.get('buscar_nome'))

        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "rg":
            queryset = queryset.filter(atendimento__paciente__rg=self.request.GET.get('buscar_nome'))

        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "sus":
            queryset = queryset.filter(atendimento__paciente__cartao_sus=self.request.GET.get('buscar_nome'))

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        context['esperando_chamadas'] = self.get_queryset().filter(
            tipo=ListaChamadaSolicitacaoAtendimento.EXAME_LABORATORIO,
            situacao=ListaChamadaSolicitacaoAtendimento.EM_ESPERA
        ).order_by(
            Case(
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=4, then=Value(0)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=3, then=Value(1)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=2, then=Value(2)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=1, then=Value(3)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=0, then=Value(4)),
                default=Value(4),
                output_field=IntegerField(),
            ),
            'atendimento__paciente__data_nascimento'
        )

        context['listagem_chamadas'] = self.get_queryset().filter(
            situacao__in=[
                ListaChamadaSolicitacaoAtendimento.DESIGNADO,
                ListaChamadaSolicitacaoAtendimento.EM_ATENDIMENTO,
                ListaChamadaSolicitacaoAtendimento.REABERTURA
            ],
        ).order_by(
            Case(
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=4, then=Value(0)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=3, then=Value(1)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=2, then=Value(2)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=1, then=Value(3)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=0, then=Value(4)),
                default=Value(4),
                output_field=IntegerField(),
            ),
            'atendimento__paciente__data_nascimento'
        )
        context['buscar_nome'] = self.request.GET.get('buscar_nome', "")
        context['opcao_filtro'] = self.request.GET.get('opcao_filtro', "") if self.request.GET.get('opcao_filtro', "") else "paciente"

        return context
    
class ExamesLaboratoriaisChamadoUpdateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, UpdateView):
    model = ListaChamadaSolicitacaoAtendimento
    required_permissions = [settings.DESENVOLVEDOR, settings.ENFERMEIRO, settings.TECNICO_ENFERMAGEM, settings.ADMINISTRADO]

    def get(self, request, *args, **kwargs):
        enfermeiro = self.request.user.profissional_set.first()

        lista_chamada = self.get_object()
        lista_chamada.situacao = ListaChamadaSolicitacaoAtendimento.DESIGNADO
        lista_chamada.sala = self.request.user.get_unidade_login().sala
        lista_chamada.tempo_espera = tempo_medio_espera_data_hora(lista_chamada.created_at)
        lista_chamada.enfermeiro=enfermeiro
        lista_chamada.contagem = 1
        lista_chamada.save()
        
        return redirect('saude_enfermagem:exames_laboratoriais_list')
    
class ExamesLaboratoriaisDetailView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, DetailView):
    model = ListaChamadaSolicitacaoAtendimento
    required_permissions = [settings.DESENVOLVEDOR, settings.ENFERMEIRO, settings.TECNICO_ENFERMAGEM, settings.ADMINISTRADO]
    template_name = 'saude_enfermagem/exames_laboratoriais_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        solicitacao, created = SolicitacaoAtendimento.objects.get_or_create(lista_chamada_solicitacao=self.object)

        if created:
            self.object.situacao = ListaChamadaSolicitacaoAtendimento.EM_ATENDIMENTO
            self.object.save()
            
        if solicitacao and not self.request.user.profissional_set.first() in solicitacao.enfermeiros.all():
            solicitacao.enfermeiros.add(self.request.user.profissional_set.first())
            solicitacao.save()

        context['ultimo_atendimento'] = BoletimPaciente.objects.filter(paciente=self.object.atendimento.paciente).exclude(
            situacao__in=[BoletimPaciente.EM_ABERTO, BoletimPaciente.EM_ANDAMENTO]).order_by('-created_at').first() 

        return context
    
class ExamesImagemListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    model = ListaChamadaSolicitacaoAtendimento
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.RADIOLOGISTA, settings.TECNICO_ENFERMAGEM, settings.ENFERMEIRO]
    template_name = "saude_enfermagem/exames_imagem_list.html"

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if not request.user.is_authenticated or request.user.is_anonymous:
            return response
        
        if self.request.user.tipo_usuario == 'desenvolvedor' or self.request.user.tipo_usuario == 'administrador':
            if not self.request.user.get_unidade_login().sala:
                messages.warning(request, 'Selecione uma sala de radiologia antes de iniciar os atendimentos!')
                params = {'setor': '12'}
                url = f"{reverse('saude:selecao_salas_list')}?{urlencode(params)}"
                
                return redirect(url)
            
            elif self.request.user.get_unidade_login().sala.unidade_setor.tipo != UnidadeSetor.RADIOLOGIA :
                messages.warning(request, 'Você precisa selecionar uma sala de radiologia antes de iniciar os atendimentos!')
                params = {'setor': '12'}
                url = f"{reverse('saude:selecao_salas_list')}?{urlencode(params)}"

                return redirect(url)
            
        if self.request.user.tipo_usuario == 'radiologista':
            if not request.user.get_unidade_login().sala:
                messages.warning(request, 'Selecione uma sala de radiologia antes de iniciar os atendimentos!')
                params = {'setor': '12'}
                url = f"{reverse('saude:selecao_salas_list')}?{urlencode(params)}"

                return redirect(url)
            
            elif self.request.user.get_unidade_login().sala.unidade_setor.tipo != UnidadeSetor.RADIOLOGIA :
                messages.warning(request, 'Você precisa selecionar uma sala de radiologia antes de iniciar os atendimentos!')
               
                params = {'setor': '12'}
                url = f"{reverse('saude:selecao_salas_list')}?{urlencode(params)}"

                return redirect(url)
            
        return super(ExamesImagemListView, self).dispatch(request, *args, **kwargs)
             
    def get_queryset(self):
        queryset = super().get_queryset().filter(tipo=ListaChamadaSolicitacaoAtendimento.EXAME_IMAGEM, unidade_saude=self.request.user.get_unidade_login().unidade)

        if self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "paciente":
            queryset = queryset.filter(atendimento__paciente__nome_paciente__icontains=self.request.GET.get('buscar_nome'))
            
        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "cpf":
            queryset = queryset.filter(atendimento__paciente__cpf=self.request.GET.get('buscar_nome'))

        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "rg":
            queryset = queryset.filter(atendimento__paciente__rg=self.request.GET.get('buscar_nome'))

        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "sus":
            queryset = queryset.filter(atendimento__paciente__cartao_sus=self.request.GET.get('buscar_nome'))

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        context['esperando_chamadas'] = self.get_queryset().filter(
            situacao=ListaChamadaSolicitacaoAtendimento.EM_ESPERA,
        ).order_by(
            Case(
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=4, then=Value(0)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=3, then=Value(1)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=2, then=Value(2)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=1, then=Value(3)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=0, then=Value(4)),
                default=Value(4),
                output_field=IntegerField(),
            ),
            'atendimento__paciente__data_nascimento'
        )

        context['listagem_chamadas'] = self.get_queryset().filter(
            situacao__in=[
                ListaChamadaSolicitacaoAtendimento.DESIGNADO,
                ListaChamadaSolicitacaoAtendimento.EM_ATENDIMENTO,
                ListaChamadaSolicitacaoAtendimento.REABERTURA
            ],
        ).order_by(
            Case(
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=4, then=Value(0)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=3, then=Value(1)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=2, then=Value(2)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=1, then=Value(3)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=0, then=Value(4)),
                default=Value(4),
                output_field=IntegerField(),
            ),
            'atendimento__paciente__data_nascimento'
        )
        context['buscar_nome'] = self.request.GET.get('buscar_nome', "")
        context['opcao_filtro'] = self.request.GET.get('opcao_filtro', "") if self.request.GET.get('opcao_filtro', "") else "paciente"

        return context
    
class ExamesImagemChamadoUpdateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, UpdateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.RADIOLOGISTA, settings.TECNICO_ENFERMAGEM, settings.ENFERMEIRO]

    def get(self, request, *args, **kwargs):
        enfermeiro = self.request.user.profissional_set.first()

        lista_chamada = ListaChamadaSolicitacaoAtendimento.objects.get(pk=kwargs.get('pk'))
        lista_chamada.situacao = ListaChamadaSolicitacaoAtendimento.DESIGNADO
        lista_chamada.sala = self.request.user.get_unidade_login().sala
        lista_chamada.tempo_espera = tempo_medio_espera_data_hora(lista_chamada.created_at)
        lista_chamada.enfermeiro=enfermeiro
        lista_chamada.contagem = 1
        lista_chamada.save()
        
        return redirect('saude_enfermagem:exames_imagem_list')

class ExamesImagemDetailView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, DetailView):
    model = ListaChamadaSolicitacaoAtendimento
    required_permissions = [settings.DESENVOLVEDOR, settings.ADMINISTRADO, settings.RADIOLOGISTA, settings.TECNICO_ENFERMAGEM, settings.ENFERMEIRO]
    template_name = 'saude_enfermagem/exames_imagem_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        solicitacao, created = SolicitacaoAtendimento.objects.get_or_create(lista_chamada_solicitacao=self.object)

        if created:
            self.object.situacao = ListaChamadaSolicitacaoAtendimento.EM_ATENDIMENTO
            self.object.save()
            
        if solicitacao and self.request.user.profissional_set.first() not in solicitacao.enfermeiros.all():
            solicitacao.enfermeiros.add(self.request.user.profissional_set.first())
            solicitacao.save()

        context['ultimo_atendimento'] = BoletimPaciente.objects.filter(paciente=self.object.atendimento.paciente).exclude(
            situacao__in=[BoletimPaciente.EM_ABERTO, BoletimPaciente.EM_ANDAMENTO]).order_by('-created_at').first()  

        return context

class AdministacaoMedicacaoListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    model = ListaChamadaSolicitacaoAtendimento
    required_permissions = [settings.DESENVOLVEDOR, settings.ENFERMEIRO, settings.TECNICO_ENFERMAGEM, settings.ADMINISTRADO]
    template_name = "saude_enfermagem/administracao_medicacao_list.html"

    def dispatch(self, request, *args, **kwargs):
        menu = self.request.GET.get('menu', "")

        response = super().dispatch(request, *args, **kwargs)
        if not request.user.is_authenticated or request.user.is_anonymous:
            return response

        if self.request.user.tipo_usuario == 'desenvolvedor' or self.request.user.tipo_usuario == 'administrador':
            if not self.request.user.get_unidade_login().sala:
                messages.warning(request, 'Selecione uma enfermaria antes de iniciar os atendimentos!')
                params = {'setor': '3'}
               
                url = f"{reverse('saude:selecao_salas_list')}?{urlencode(params)}&{urlencode({'menu': menu})}"

                return redirect(url)
            
            elif self.request.user.get_unidade_login().sala.unidade_setor.tipo != UnidadeSetor.ENFERMARIA :
                messages.warning(request, 'Você precisa selecionar uma enfermaria antes de iniciar os atendimentos!')
                params = {'setor': '3'}
                
                url = f"{reverse('saude:selecao_salas_list')}?{urlencode(params)}&{urlencode({'menu': menu})}"

                return redirect(url)
            
        if self.request.user.tipo_usuario == 'enfermeiro' or self.request.user.tipo_usuario == 'tecnico_enfermagem':
            if not request.user.get_unidade_login().sala:
                messages.warning(request, 'Selecione uma enfermaria antes de iniciar os atendimentos!')
                params = {'setor': '3'}
               
                url = f"{reverse('saude:selecao_salas_list')}?{urlencode(params)}&{urlencode({'menu': menu})}"

                return redirect(url)
            
            elif self.request.user.get_unidade_login().sala.unidade_setor.tipo != UnidadeSetor.ENFERMARIA :
                messages.warning(request, 'Você precisa selecionar uma enfermaria antes de iniciar os atendimentos!')
                params = {'setor': '3'}
               
                url = f"{reverse('saude:selecao_salas_list')}?{urlencode(params)}&{urlencode({'menu': menu})}"

                return redirect(url)
            
        return super(AdministacaoMedicacaoListView, self).dispatch(request, *args, **kwargs)
             
    def get_queryset(self):
        queryset = super().get_queryset().filter(tipo=ListaChamadaSolicitacaoAtendimento.MEDICACAO, unidade_saude=self.request.user.get_unidade_login().unidade)

        if self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "paciente":
            queryset = queryset.filter(atendimento__paciente__nome_paciente__icontains=self.request.GET.get('buscar_nome'))
            
        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "cpf":
            queryset = queryset.filter(atendimento__paciente__cpf=self.request.GET.get('buscar_nome'))

        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "rg":
            queryset = queryset.filter(atendimento__paciente__rg=self.request.GET.get('buscar_nome'))

        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "sus":
            queryset = queryset.filter(atendimento__paciente__cartao_sus=self.request.GET.get('buscar_nome'))

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        context['esperando_chamadas'] = self.get_queryset().filter(
            situacao=ListaChamadaSolicitacaoAtendimento.EM_ESPERA,
        ).order_by(
            Case(
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=4, then=Value(0)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=3, then=Value(1)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=2, then=Value(2)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=1, then=Value(3)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=0, then=Value(4)),
                default=Value(4),
                output_field=IntegerField(),
            ),
            'atendimento__paciente__data_nascimento'
        )

        context['listagem_aguardando_administracao_medicacao'] = ListaChamadoAdministracaoMedicamento.objects.filter(
            situacao=ListaChamadoAdministracaoMedicamento.EM_ESPERA,
            boletim__tipo = BoletimPaciente.MEDICACAO,
        ).order_by('updated_at')


        context['listagem_chamadas'] = self.get_queryset().filter(
            situacao__in=[
                ListaChamadaSolicitacaoAtendimento.DESIGNADO,
                ListaChamadaSolicitacaoAtendimento.EM_ATENDIMENTO,
                ListaChamadaSolicitacaoAtendimento.REABERTURA
            ],
        ).order_by(
            Case(
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=4, then=Value(0)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=3, then=Value(1)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=2, then=Value(2)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=1, then=Value(3)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=0, then=Value(4)),
                default=Value(4),
                output_field=IntegerField(),
            ),
            'atendimento__paciente__data_nascimento'
        )

        context['lista_chamado_administracao_medicamento'] = ListaChamadoAdministracaoMedicamento.objects.filter(
            situacao=ListaChamadoAdministracaoMedicamento.DESIGNADO,
            boletim__tipo = BoletimPaciente.MEDICACAO,
        ).order_by('updated_at')
        

        context['data_hora_atual'] = timezone.localtime(timezone.now())
        context['buscar_nome'] = self.request.GET.get('buscar_nome', "")
        context['opcao_filtro'] = self.request.GET.get('opcao_filtro', "") if self.request.GET.get('opcao_filtro', "") else "paciente"
        context['crumbs'] = [
            {'label': 'Admin de Medicação', 'url': reverse('saude_enfermagem:administracao_medicacao_list')},
        ]

        return context
    
class AdministracaoMedicacaoVacinaCreateView(CheckUserTypeMixin, LoginRequiredMixin, TemplateView):
    template_name = 'saude_enfermagem/administracao_medicacao_vacina_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solicitacao_id = self.request.GET.get('solicitacao')

        context['solicitacao'] = ListaChamadoAdministracaoMedicamento.objects.get(id=solicitacao_id)
        context['unidade_saude_session_id'] = self.request.user.get_unidade_login().unidade.id
        context['enfermeiro'] = Profissional.objects.get(user=self.request.user)

        return context

class AdministacaoMedicacaoChamadoUpdateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, UpdateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ENFERMEIRO, settings.TECNICO_ENFERMAGEM, settings.ADMINISTRADO]

    def get(self, request, *args, **kwargs):
        enfermeiro = self.request.user.profissional_set.first()
        
        lista_chamada = ListaChamadaSolicitacaoAtendimento.objects.get(pk=kwargs.get('pk'))
        lista_chamada.situacao = ListaChamadaSolicitacaoAtendimento.DESIGNADO
        lista_chamada.tempo_espera = tempo_medio_espera_data_hora(lista_chamada.created_at)
        lista_chamada.sala = self.request.user.get_unidade_login().sala
        lista_chamada.enfermeiro=enfermeiro
        lista_chamada.contagem = 1
        lista_chamada.save()
        
        return redirect('saude_enfermagem:administracao_medicacao_list')
    
class AdministracaoMedicamentoVacinaUpdateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, UpdateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ENFERMEIRO, settings.TECNICO_ENFERMAGEM, settings.ADMINISTRADO]

    def get(self, request, *args, **kwargs):
        enfermeiro = self.request.user.profissional_set.first()
        
        lista_chamada = ListaChamadoAdministracaoMedicamento.objects.get(pk=kwargs.get('pk'))
        lista_chamada.situacao = ListaChamadoAdministracaoMedicamento.DESIGNADO
        lista_chamada.sala = self.request.user.get_unidade_login().sala
        lista_chamada.enfermeiro=enfermeiro
        lista_chamada.contagem = 1
        lista_chamada.save()
        
        return redirect('saude_enfermagem:administracao_medicacao_list') 

class AdministracaoMedicamentoVacinaEmAbertoListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    model = ListaChamadoAdministracaoMedicamento
    required_permissions = [settings.DESENVOLVEDOR, settings.MEDICO, settings.ADMINISTRADO, settings.TECNICO_ENFERMAGEM, settings.ENFERMEIRO]
    template_name = "saude_enfermagem/administracao_medicacao_vacina_em_aberto_list.html"

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            sala=self.request.user.get_unidade_login().sala,
            unidade_saude=self.request.user.get_unidade_login().unidade,
            situacao__in=[ListaChamadoAdministracaoMedicamento.EM_ATENDIMENTO, ListaChamadoAdministracaoMedicamento.EM_ATENDIMENTO_RETORNO]
        )

        if self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "paciente":
            queryset = queryset.filter(boletim__paciente__nome_paciente__icontains=self.request.GET.get('buscar_nome'))
            
        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "cpf":
            queryset = queryset.filter(boletim__paciente__cpf=self.request.GET.get('buscar_nome'))

        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "rg":
            queryset = queryset.filter(boletim__paciente__rg=self.request.GET.get('buscar_nome'))

        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "sus":
            queryset = queryset.filter(boletim__paciente__cartao_sus=self.request.GET.get('buscar_nome'))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buscar_nome'] = self.request.GET.get('buscar_nome', "")
        context['opcao_filtro'] = self.request.GET.get('opcao_filtro', "") if self.request.GET.get('opcao_filtro', "") else "paciente"
        
        return context
    
class AdministracaoMedicacaoDetailView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, DetailView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ENFERMEIRO, settings.TECNICO_ENFERMAGEM, settings.ADMINISTRADO]
    model = ListaChamadaSolicitacaoAtendimento
    template_name = 'saude_enfermagem/administracao_medicacao_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        solicitacao, created = SolicitacaoAtendimento.objects.get_or_create(lista_chamada_solicitacao=self.object)

        if created:
            self.object.situacao = ListaChamadaSolicitacaoAtendimento.EM_ATENDIMENTO
            self.object.save()
            
        if solicitacao and not self.request.user.profissional_set.first() in solicitacao.enfermeiros.all():
            solicitacao.enfermeiros.add(self.request.user.profissional_set.first())
            solicitacao.save()

        context['ultimo_atendimento'] = BoletimPaciente.objects.filter(paciente=self.object.atendimento.paciente).exclude(
            situacao__in=[BoletimPaciente.EM_ABERTO, BoletimPaciente.EM_ANDAMENTO]).order_by('-created_at').first()   

        return context
    
class ProcedimentosListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ENFERMEIRO, settings.TECNICO_ENFERMAGEM, settings.ADMINISTRADO]
    model = ListaChamadaSolicitacaoAtendimento
    template_name = "saude_enfermagem/procedimentos_list.html"

    def dispatch(self, request, *args, **kwargs):
        menu = self.request.GET.get('menu', "")

        response = super().dispatch(request, *args, **kwargs)
        if not request.user.is_authenticated or request.user.is_anonymous:
            return response

        if self.request.user.tipo_usuario == 'desenvolvedor' or self.request.user.tipo_usuario == 'administrador':
            if not self.request.user.get_unidade_login().sala:
                messages.warning(request, 'Selecione uma enfermaria antes de iniciar os atendimentos!')
                params = {'setor': '3'}
               
                url = f"{reverse('saude:selecao_salas_list')}?{urlencode(params)}&{urlencode({'menu': menu})}"

                return redirect(url)
            
            elif self.request.user.get_unidade_login().sala.unidade_setor.tipo != UnidadeSetor.ENFERMARIA :
                messages.warning(request, 'Você precisa selecionar uma enfermaria antes de iniciar os atendimentos!')
                params = {'setor': '3'}
                
                url = f"{reverse('saude:selecao_salas_list')}?{urlencode(params)}&{urlencode({'menu': menu})}"

                return redirect(url)
            
        if self.request.user.tipo_usuario == 'enfermeiro' or self.request.user.tipo_usuario == 'tecnico_enfermagem':
            if not request.user.get_unidade_login().sala:
                messages.warning(request, 'Selecione uma enfermaria antes de iniciar os atendimentos!')
                params = {'setor': '3'}
               
                url = f"{reverse('saude:selecao_salas_list')}?{urlencode(params)}&{urlencode({'menu': menu})}"

                return redirect(url)
            
            elif self.request.user.get_unidade_login().sala.unidade_setor.tipo != UnidadeSetor.ENFERMARIA :
                messages.warning(request, 'Você precisa selecionar uma enfermaria antes de iniciar os atendimentos!')
                params = {'setor': '3'}
               
                url = f"{reverse('saude:selecao_salas_list')}?{urlencode(params)}&{urlencode({'menu': menu})}"

                return redirect(url)
            
        return super(ProcedimentosListView, self).dispatch(request, *args, **kwargs)
             
    def get_queryset(self):
        queryset = super().get_queryset().filter(tipo=ListaChamadaSolicitacaoAtendimento.PROCEDIMENTO, unidade_saude=self.request.user.get_unidade_login().unidade)

        if self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "paciente":
            queryset = queryset.filter(atendimento__paciente__nome_paciente__icontains=self.request.GET.get('buscar_nome'))
            
        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "cpf":
            queryset = queryset.filter(atendimento__paciente__cpf=self.request.GET.get('buscar_nome'))

        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "rg":
            queryset = queryset.filter(atendimento__paciente__rg=self.request.GET.get('buscar_nome'))

        elif self.request.GET.get('buscar_nome') and self.request.GET.get('opcao_filtro') == "sus":
            queryset = queryset.filter(atendimento__paciente__cartao_sus=self.request.GET.get('buscar_nome'))

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        context['esperando_chamadas'] = self.get_queryset().filter(
            situacao=ListaChamadaSolicitacaoAtendimento.EM_ESPERA,
        ).order_by(
            Case(
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=4, then=Value(0)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=3, then=Value(1)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=2, then=Value(2)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=1, then=Value(3)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=0, then=Value(4)),
                default=Value(4),
                output_field=IntegerField(),
            ),
            'atendimento__paciente__data_nascimento'
        )

        context['listagem_chamadas'] = self.get_queryset().filter(
            situacao__in=[
                ListaChamadaSolicitacaoAtendimento.DESIGNADO, 
                ListaChamadaSolicitacaoAtendimento.EM_ATENDIMENTO,
                ListaChamadaSolicitacaoAtendimento.REABERTURA, 
            ],
        ).order_by(
            Case(
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=4, then=Value(0)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=3, then=Value(1)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=2, then=Value(2)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=1, then=Value(3)),
                When(atendimento__lista_chamada__classificacao_risco__tipo_classificacao_risco__tipo=0, then=Value(4)),
                default=Value(4),
                output_field=IntegerField(),
            ),
            'atendimento__paciente__data_nascimento'
        )

        context['aguardando_atendimento_eletivo'] = ListaChamadoAdministracaoProcedimento.objects.filter(
            Q(situacao=ListaChamadoAdministracaoProcedimento.DESIGNADO) | 
            Q(situacao=ListaChamadoAdministracaoProcedimento.EM_ESPERA),
            classificacao_risco__tipo_fluxo = ClassificacaoRisco.FLUXO_PROCEDIMENTO,
        ).order_by('updated_at')

        context['paciente_designado_eletivo'] = ListaChamadoAdministracaoProcedimento.objects.filter(
            situacao=ListaChamadoAdministracaoProcedimento.EM_ATENDIMENTO,
            classificacao_risco__tipo_fluxo = ClassificacaoRisco.FLUXO_PROCEDIMENTO,
        ).order_by('updated_at')

        context['data_hora_atual'] = timezone.localtime(timezone.now())
        context['buscar_nome'] = self.request.GET.get('buscar_nome', "")
        context['opcao_filtro'] = self.request.GET.get('opcao_filtro', "") if self.request.GET.get('opcao_filtro', "") else "paciente"
        context['crumbs'] = [
            {'label': 'Procedimentos Listagem', 'url': reverse('saude_enfermagem:procedimentos_list')},
        ]

        return context
    
class ProcedimentosChamadoUpdateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, UpdateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ENFERMEIRO, settings.TECNICO_ENFERMAGEM, settings.ADMINISTRADO]

    def get(self, request, *args, **kwargs):
        enfermeiro = self.request.user.profissional_set.first()
        
        lista_chamada = ListaChamadaSolicitacaoAtendimento.objects.get(pk=kwargs.get('pk'))
        lista_chamada.situacao = ListaChamadaSolicitacaoAtendimento.DESIGNADO
        lista_chamada.tempo_espera = tempo_medio_espera_data_hora(lista_chamada.created_at)
        lista_chamada.sala = self.request.user.get_unidade_login().sala
        lista_chamada.enfermeiro=enfermeiro
        lista_chamada.contagem = 1
        lista_chamada.save()
        
        return redirect('saude_enfermagem:procedimentos_list')
    
class ProcedimentosDetailView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, DetailView):
    model = ListaChamadaSolicitacaoAtendimento
    required_permissions = [settings.DESENVOLVEDOR, settings.ENFERMEIRO, settings.TECNICO_ENFERMAGEM, settings.ADMINISTRADO]
    template_name = 'saude_enfermagem/procedimentos_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        solicitacao, created = SolicitacaoAtendimento.objects.get_or_create(lista_chamada_solicitacao=self.object)

        if created:
            self.object.situacao = ListaChamadaSolicitacaoAtendimento.EM_ATENDIMENTO
            self.object.save()
            
        if solicitacao and self.request.user.profissional_set.first():
            solicitacao.enfermeiros.add(self.request.user.profissional_set.first())
            solicitacao.save()

        context['ultimo_atendimento'] = BoletimPaciente.objects.filter(paciente=self.object.atendimento.paciente).exclude(
            situacao__in=[BoletimPaciente.EM_ABERTO, BoletimPaciente.EM_ANDAMENTO]).order_by('-created_at').first()   

        return context

class AtendimentosRealizadosListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    model = ListaChamadaSolicitacaoAtendimento
    required_permissions = [settings.DESENVOLVEDOR, settings.ENFERMEIRO, settings.TECNICO_ENFERMAGEM]
    template_name = 'saude_enfermagem/atendimentos_efetuados_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new_date = dt.now()

        context['crumbs'] = [{'label': 'Listagem de Atendimentos', 'url': '#'},]

        context['data_inicial_filtro'] = self.request.GET.get('data_inicial_filtro', '')
        if not self.request.GET.get('data_inicial_filtro', ''):
            context['data_inicial_filtro'] = new_date.strftime("%Y-%m-%d")

        context['data_final_filtro'] = self.request.GET.get('data_final_filtro', '')
        if not self.request.GET.get('data_final_filtro', ''):
            context['data_final_filtro'] = new_date.strftime("%Y-%m-%d")

        context['hora_inicial_filtro'] = self.request.GET.get('hora_inicial_filtro', '')
        context['hora_final_filtro'] = self.request.GET.get('hora_final_filtro', '')

        data_inicial_filtro = self.request.GET.get('data_inicial_filtro') if self.request.GET.get('data_inicial_filtro') else new_date.strftime("%Y-%m-%d")
        data_final_filtro = self.request.GET.get('data_final_filtro') if self.request.GET.get('data_final_filtro') else new_date.strftime("%Y-%m-%d")

        profissional = Profissional.objects.get(user=self.request.user)

        classificacoes_risco = ClassificacaoRisco.objects.filter(
            profissional=profissional,
            status=ClassificacaoRisco.ATIVO,
            created_at__date__range=(data_inicial_filtro, data_final_filtro),
        ).values_list('paciente__id', 'created_at', 'paciente__nome_paciente', 'tipo_classificacao_risco__tipo', 'boletim').distinct()

        lista_chamada_solicitacao = SolicitacaoAtendimento.objects.filter(
            enfermeiros__isnull=False,
            enfermeiros__in=[profissional.id],
            lista_chamada_solicitacao__tipo=ListaChamadaSolicitacaoAtendimento.MEDICACAO,
            lista_chamada_solicitacao__historicoesperasolicitacoes__situacao=ListaChamadaSolicitacaoAtendimento.CONCLUIDO,
            lista_chamada_solicitacao__created_at__date__range=(data_inicial_filtro, data_final_filtro),
        ).order_by('lista_chamada_solicitacao__atendimento__paciente__nome_paciente', 'enfermeiros').distinct('lista_chamada_solicitacao__atendimento__paciente__nome_paciente')

        pacientes_adicionados = set()
        listas = []
        for classificacao in classificacoes_risco:
            paciente_id = classificacao[0]
            if paciente_id not in pacientes_adicionados:
                listas.append({
                    'data': timezone.localtime(classificacao[1]).strftime("%d/%m/%Y"),
                    'paciente_nome': classificacao[2],
                    'classificacao_risco': classificacao[3],
                })
                pacientes_adicionados.add(paciente_id)

        for solicitacao in lista_chamada_solicitacao:
            paciente_id = solicitacao.lista_chamada_solicitacao.atendimento.paciente.id
            if paciente_id not in pacientes_adicionados:
                listas.append({
                    'data': timezone.localtime(solicitacao.created_at).strftime("%d/%m/%Y"),
                    'paciente_nome': solicitacao.lista_chamada_solicitacao.atendimento.paciente.nome_paciente,
                    'classificacao_risco': solicitacao.lista_chamada_solicitacao.atendimento.lista_chamada.classificacao_risco.tipo_classificacao_risco.tipo,
                })
                pacientes_adicionados.add(paciente_id)

        context['listas'] = listas

        return context

class AtendimentosRealizadosPDFView(CheckUserTypeMixin, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data_inicial_filtro = self.request.GET.get('data_inicial_filtro', '')
        data_final_filtro = self.request.GET.get('data_final_filtro', '')
        hora_inicial_filtro = self.request.GET.get('hora_inicial_filtro', '')
        hora_final_filtro = self.request.GET.get('hora_final_filtro', '')

        profissional = Profissional.objects.get(user=self.request.user)

        new_date = dt.now()

        classificacoes_risco = ClassificacaoRisco.objects.filter(
            profissional=profissional,
            status=ClassificacaoRisco.ATIVO,
            created_at__date__range=(data_inicial_filtro, data_final_filtro)
        ).distinct('boletim')

        lista_producao = {}
        for classificacao in classificacoes_risco:
            paciente_id = classificacao.paciente.id
            if paciente_id not in lista_producao:
                lista_producao[paciente_id] = {
                    'paciente_nome': classificacao.paciente.nome_paciente,
                    'paciente_idade': classificacao.paciente.calcular_idade(),
                    'profissional_cns': classificacao.profissional.cns,
                    'classificacao': True,
                    'ambulatorio': False,
                    'pressao': True if classificacao.presao_arterial else False,
                    'temperatura': True if classificacao.temperatura else False,
                    'antropometria': False,
                    'alivio': False,
                    'demora': False,
                    'oxigenoterapia': False,
                    'especial': False,
                    'grau': False,
                    'pontos': False,
                    'gilcemia': False,
                    'hiv': False,
                    'sifilis': False,
                    'hbs': False,
                    'sars': False,
                    'medicacao': False,
                    'distorcia': False,
                    'normal': False,
                    'nascido': False,
                    'reidratacao': False,
                    'nebulizacao': False,
                    'ecg': False,
                    'curativo_simples': False,
                    'cateter': False,
                    'enema': False,
                    'transferencia': False,
                }
            else:
                lista_producao[paciente_id]['pressao'] = lista_producao[paciente_id]['pressao'] or (True if classificacao.presao_arterial else False)
                lista_producao[paciente_id]['temperatura'] = lista_producao[paciente_id]['temperatura'] or (True if classificacao.temperatura else False)

        lista_chamada_solicitacao = SolicitacaoAtendimento.objects.filter(
            enfermeiros__isnull=False,
            enfermeiros__in=[profissional.id],
            lista_chamada_solicitacao__tipo=ListaChamadaSolicitacaoAtendimento.MEDICACAO,
            lista_chamada_solicitacao__historicoesperasolicitacoes__situacao=ListaChamadaSolicitacaoAtendimento.CONCLUIDO,
            lista_chamada_solicitacao__created_at__date__range=(data_inicial_filtro, data_final_filtro),
        ).order_by('lista_chamada_solicitacao__atendimento__paciente__nome_paciente', 'enfermeiros').distinct('lista_chamada_solicitacao__atendimento__paciente__nome_paciente')

        for lista in lista_chamada_solicitacao:
            paciente_id = lista.lista_chamada_solicitacao.atendimento.paciente.id
            if paciente_id not in lista_producao:
                lista_producao[paciente_id] = {
                    'paciente_nome': lista.lista_chamada_solicitacao.atendimento.paciente.nome_paciente,
                    'paciente_idade': lista.lista_chamada_solicitacao.atendimento.paciente.calcular_idade(),
                    'profissional_cns': lista.enfermeiros.filter(user=self.request.user).first().cns,
                    'classificacao': False,
                    'ambulatorio': False,
                    'pressao': False,
                    'temperatura': False,
                    'antropometria': False,
                    'alivio': False,
                    'demora': False,
                    'oxigenoterapia': False,
                    'especial': False,
                    'grau': False,
                    'pontos': False,
                    'gilcemia': False,
                    'hiv': False,
                    'sifilis': False,
                    'hbs': False,
                    'sars': False,
                    'medicacao': True,
                    'distorcia': False,
                    'normal': False,
                    'nascido': False,
                    'reidratacao': False,
                    'nebulizacao': False,
                    'ecg': False,
                    'curativo_simples': False,
                    'cateter': False,
                    'enema': False,
                    'transferencia': False,
                }
            else:
                lista_producao[paciente_id]['medicacao'] = lista_producao[paciente_id]['medicacao'] or True

        lista_producao = list(lista_producao.values())

        html_index = render_to_string('saude_enfermagem/exportacao/atendimentos_efetuados_pdf.html', {
            'lista_producao': lista_producao,
            'data_inicial': dt.strptime(data_inicial_filtro, "%Y-%m-%d").strftime("%d/%m/%Y"),
            'data_final': dt.strptime(data_final_filtro, "%Y-%m-%d").strftime("%d/%m/%Y"),
            'hora_inicial': hora_inicial_filtro,
            'hora_final': hora_final_filtro,
            'data_impressao': new_date.strftime("%d/%m/%Y %H:%m"),
            'unidade_saude': self.request.user.get_unidade_login().unidade,
            'profissional': profissional,
            'linhas_brancas': range(5),
        })
        
        # html = weasyprint.HTML(string=html_index, base_url=request.build_absolute_uri('/media/'))

        pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        html.write_pdf(target=pdf_file.name)

        with open(pdf_file.name, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="relatorio_prestacao_contas_{new_date.strftime("%Y_%m_%d")}.pdf"'
            return response
        
class AdministracaoMedicamentoVacinaDetailView(CheckUserTypeMixin, LoginRequiredMixin, DetailView):
    model = ListaChamadoAdministracaoMedicamento
    required_permissions = [settings.DESENVOLVEDOR, settings.ENFERMEIRO, settings.TECNICO_ENFERMAGEM, settings.ADMINISTRADO]
    template_name = 'saude_enfermagem/administracao_medicacao_vacina_detail.html'  

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        response = super().dispatch(request, *args, **kwargs)
        if not request.user.is_authenticated or request.user.is_anonymous:
            return response

        if self.object.boletim.situacao not in [BoletimPaciente.EM_ABERTO, BoletimPaciente.EM_ANDAMENTO]:
            messages.warning(self.request, 'Administração de medicação selecionada foi finalizada.')
            return redirect(reverse('saude_enfermagem:administracao_medicamento_vacina_aberto_list')) 
        
        return super().dispatch(request, *args, **kwargs) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()

        if self.object.situacao == ListaChamadoAdministracaoMedicamento.DESIGNADO:
            self.object.situacao = ListaChamadoAdministracaoMedicamento.EM_ATENDIMENTO_RETORNO
            self.object.save()

        context['receita_medicamento'] = ReceitaMedicamento.objects.filter(lista_chamada_solicitacao__id=self.object.id).first()
        context['enfermeiro'] = Profissional.objects.get(user=self.request.user)

        return context

class AdministracaoProcedimentosListView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, ListView):
    model = ListaChamadoAdministracaoProcedimento
    required_permissions = [settings.DESENVOLVEDOR, settings.MEDICO, settings.ADMINISTRADO, settings.TECNICO_ENFERMAGEM, settings.ENFERMEIRO]
    template_name = "saude_enfermagem/administracao_procedimentos_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        context['aguardando_atendimento'] = ListaChamadoAdministracaoProcedimento.objects.filter(
            situacao=ListaChamadoAdministracaoProcedimento.EM_ESPERA,
            classificacao_risco__tipo_fluxo = ClassificacaoRisco.FLUXO_PROCEDIMENTO,
        ).order_by('updated_at')

        context['paciente_designado'] = ListaChamadoAdministracaoProcedimento.objects.filter(
            situacao=ListaChamadoAdministracaoProcedimento.DESIGNADO,
            classificacao_risco__tipo_fluxo = ClassificacaoRisco.FLUXO_PROCEDIMENTO,
        ).order_by('updated_at')

        context['data_hora_atual'] = timezone.localtime(timezone.now())
        context['buscar_nome'] = self.request.GET.get('buscar_nome', "")
        context['opcao_filtro'] = self.request.GET.get('opcao_filtro', "") if self.request.GET.get('opcao_filtro', "") else "paciente"
        context['crumbs'] = [
            {'label': 'Admin de Procedimento', 'url': reverse('saude_enfermagem:administracao_procedimentos_list')},
        ]

        return context

class AdministracaoProcedimentoUpdateView(CheckUserTypeMixin, LoginRequiredMixin, SaudeCheckHasPermission, UpdateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ENFERMEIRO, settings.TECNICO_ENFERMAGEM, settings.ADMINISTRADO]

    def get(self, request, *args, **kwargs):
        enfermeiro = self.request.user.profissional_set.first()
        
        lista_chamada = ListaChamadoAdministracaoProcedimento.objects.get(pk=kwargs.get('pk'))
        lista_chamada.situacao = ListaChamadoAdministracaoProcedimento.EM_ATENDIMENTO
        lista_chamada.sala = self.request.user.get_unidade_login().sala
        lista_chamada.enfermeiro=enfermeiro
        lista_chamada.contagem = 1
        lista_chamada.save()
        
        return redirect('saude_enfermagem:procedimentos_list') 

class AdministracaoProcedimentoCreateView(CheckUserTypeMixin, LoginRequiredMixin, DetailView):
    model = ListaChamadoAdministracaoProcedimento
    required_permissions = [settings.DESENVOLVEDOR, settings.ENFERMEIRO, settings.TECNICO_ENFERMAGEM, settings.ADMINISTRADO]
    template_name = 'saude_enfermagem/administracao_procedimentos_create.html'  

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        response = super().dispatch(request, *args, **kwargs)
        if not request.user.is_authenticated or request.user.is_anonymous:
            return response

        if self.object.classificacao_risco.boletim.situacao not in [BoletimPaciente.EM_ABERTO, BoletimPaciente.EM_ANDAMENTO]:
            messages.warning(self.request, 'Administração de Procedimento selecionada foi finalizada.')
            return redirect('saude_enfermagem:administracao_procedimento_create', pk=object.pk)
        
        return super().dispatch(request, *args, **kwargs) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()

        # if self.object.situacao == ListaChamadoAdministracaoProcedimento.DESIGNADO:
        #     self.object.situacao = ListaChamadoAdministracaoProcedimento.EM_ATENDIMENTO
        #     self.object.save()

        context['solicitacao'] = ListaChamadoAdministracaoProcedimento.objects.get(id=self.object.id)
        context['receita_medicamento'] = ReceitaMedicamento.objects.filter(lista_chamada_solicitacao__id=self.object.id).first()
        context['unidade_saude_session_id'] = self.request.user.get_unidade_login().unidade.id
        context['enfermeiro'] = Profissional.objects.get(user=self.request.user)

        return context

class AdministracaoProcedimentoDetailView(CheckUserTypeMixin, LoginRequiredMixin, DetailView):
    model = ListaChamadoAdministracaoProcedimento
    required_permissions = [settings.DESENVOLVEDOR, settings.ENFERMEIRO, settings.TECNICO_ENFERMAGEM, settings.ADMINISTRADO]
    template_name = 'saude_enfermagem/administracao_procedimento_detail.html'  

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        response = super().dispatch(request, *args, **kwargs)
        if not request.user.is_authenticated or request.user.is_anonymous:
            return response

        if self.object.classificacao_risco.boletim.situacao not in [BoletimPaciente.EM_ABERTO, BoletimPaciente.EM_ANDAMENTO]:
            messages.warning(self.request, 'Administração de Procedimento selecionada foi finalizada.')
            return redirect(reverse('saude_enfermagem:administracao_procedimentos_list')) 
        
        return super().dispatch(request, *args, **kwargs) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()

        context['lista_procedimento_id'] = str(self.object.id)
        context['get_paciente'] = ListaChamadoAdministracaoProcedimento.objects.get(id=self.object.id)
        context['receita_procedimento'] = ReceitaAdministracaoProcedimento.objects.filter(lista_chamada_solicitacao__id=self.object.id).first()
        context['unidade_saude_session_id'] = self.request.user.get_unidade_login().unidade.id

        return context