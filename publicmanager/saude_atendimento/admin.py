import csv
from django.contrib import admin
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.urls import path, reverse
from django.utils.html import format_html
from simple_history.admin import SimpleHistoryAdmin

from publicmanager.saude_atendimento.forms import RelatorioAtendimentosForm
from publicmanager.saude_enfermagem.models import SituacaoMedicacaoAtendimento
from .models import (
    Paciente, TipoAltaHospitalar, BoletimPaciente, EvolucaoAtendimento,
    AnamnesePaciente, ClassificacaoRisco, ListaChamada, AtendimentoMedico,
    DiagnosticoAtendimento, ExameAtendimento, ProcedimentoAtendimento, MedicacaoAtendimento,
    DocumentoPaciente, AtestadoAtendimento, FichaReferenciaAtendimento, AgendamentoConsultorio, 
    HistoricoEsperaAtendimento, Feriado, BloqueioAgenda, HorarioMedico, JustificativaProcedimentoAtendimento,
    ListaChamadaClassificacaoRisco, ArquivoExameAtendimento, ReaberturaAtendimentoMedico, ArquivoProcedimentoAtendimento
)

@admin.register(Paciente)
class PacienteAdmin(SimpleHistoryAdmin):
    list_display= ('nome_paciente', 'cartao_sus', 'cpf', 'rg')
    search_fields = ('nome_paciente',)
    readonly_fields = ['anamnese_paciente',]

    fieldsets = (
        (None, {'fields': ('nome_paciente', 'foto_paciente', 'nome_social', 'nome_mae', 'nome_pai', 'data_nascimento',
            'naturalidade', 'nacionalidade', 'raca', 'sexo', 'estado_civil', 'grau_de_instrucao', 'profissao',
            'grupo_sanguineo', 'fator_rh', 'doador_sanguineo', 'doador_de_orgaos')}),
        ('Dados Pessoais', { 'fields': ('cartao_sus', 'cpf', 'rg', 'rg_orgao', 'rg_uf', 'rg_data', 'situacao')}),
        ('Contado', { 'fields': ('celular', 'telefone_fixo', 'whatsapp', 'email')}),
        ('Endereço', { 'fields': ('cep', 'endereco', 'numero', 'complemento', 'bairro', 'estado', 'municipio')}),
        (None, { 'fields': ('anamnese_paciente',)}),
    )

@admin.register(ListaChamadaClassificacaoRisco)
class ListaChamadaClassificacaoRiscoAdmin(admin.ModelAdmin):
    list_display= ('nome_paciente', 'boletim', 'unidade_saude', 'contagem', 'situacao')
    search_fields = ('boletim__paciente__nome_paciente',)

    def nome_paciente(self, obj):
        if obj.boletim.paciente:
            return obj.boletim.paciente.nome_paciente
        return None

@admin.register(DocumentoPaciente)
class DocumentoPacienteAdmin(admin.ModelAdmin):
    list_display= ('paciente', 'nome')

@admin.register(AnamnesePaciente)
class AnamnesePacienteAdmin(SimpleHistoryAdmin):
    list_display= ('paciente_nome', 'id', 'created_at')
    search_fields = ('id', 'paciente__nome_paciente')
    ordering = ["-created_at"]

@admin.register(BoletimPaciente)
class BoletimPacienteAdmin(SimpleHistoryAdmin):
    list_display= ('paciente', 'data_entrada', 'situacao', 'data_entrada', 'data_saida', 'unidade_saude', 'tipo')
    search_fields = ('paciente__nome_paciente', 'profissional__nome_profissional')
    ordering = ["-created_at"]

@admin.register(TipoAltaHospitalar)
class TipoAltaHospitalarAdmin(admin.ModelAdmin):
    list_display= ('id', 'situacao')
    search_fields = ('nome',)
    ordering = ["-created_at"]

@admin.register(ClassificacaoRisco)
class ClassificacaoRiscoAdmin(SimpleHistoryAdmin):
    list_display= ('paciente', 'tipo_atendimento', 'numero_atendimento', 'data_hora_avaliacao')
    search_fields = ('paciente__nome_paciente', 'profissional__nome_profissional')
    ordering = ["-created_at"]

class HistoricoEsperaAtendimentoInline(admin.TabularInline):
    model = HistoricoEsperaAtendimento
    extra = 0
    show_change_link = True
    readonly_fields = ['situacao', 'tempo_espera', 'profissional']
    ordering = ['-created_at']

@admin.register(ListaChamada)
class ListaChamadaAdmin(SimpleHistoryAdmin):
    list_display= ('paciente', 'classificacao_risco', 'situacao', 'contagem', 'updated_at')
    inlines = [HistoricoEsperaAtendimentoInline,]	
    search_fields = ('paciente__nome_paciente', 'medico__nome_profissional')

class ReaberturaAtendimentoMedicoInline(admin.TabularInline):
    model = ReaberturaAtendimentoMedico
    extra = 0
    show_change_link = True
    readonly_fields = ['atendimento', 'profissional', 'justificativa']
    ordering = ['-created_at']

@admin.register(AtendimentoMedico)
class AtendimentoMedicoAdmin(admin.ModelAdmin):
    list_display= ('paciente', 'unidade_saude', 'lista_chamada', 'created_at')
    readonly_fields = ['profissionais',]
    search_fields = ('paciente__nome_paciente',)
    ordering = ["-created_at"]
    list_filter = ('lista_chamada__situacao',)
    inlines = [ReaberturaAtendimentoMedicoInline, ]
    change_list_template = "admin/changer_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('exportar-relatorio/', self.admin_site.admin_view(self.exportar_relatorio_atendimentos), name='exportar_relatorio_atendimentos'),
        ]
        return custom_urls + urls

    def exportar_relatorio_atendimentos(self, request):
        if request.method == 'POST':
            form = RelatorioAtendimentosForm(request.POST)
            if form.is_valid():
                data_inicial = form.cleaned_data['data_inicial']
                data_final = form.cleaned_data['data_final']
                unidade_saude = form.cleaned_data['unidade_saude']

                meta = self.model._meta
                response = HttpResponse(content_type='text/txt')
                response['Content-Disposition'] = 'attachment; filename={}.txt'.format(meta)
                writer = csv.writer(response, delimiter="|", quoting=csv.QUOTE_MINIMAL)

                # Escreve o cabeçalho do CSV
                writer.writerow(['Paciente', 'Unidade de Saúde', 'Situação', 'Data de Criação', 'Data Inicial', 'Data Final', 'Unidade', 'Total'])

                total = 0
                atendimentos = AtendimentoMedico.objects.all()
                if data_inicial:
                    atendimentos = atendimentos.filter(created_at__gte=data_inicial)
                if data_final:
                    atendimentos = atendimentos.filter(created_at__lte=data_final)
                if unidade_saude:
                    atendimentos = atendimentos.filter(unidade_saude=unidade_saude)

                for atendimento in atendimentos:
                    writer.writerow([
                        atendimento.lista_chamada.paciente.nome_paciente,
                        atendimento.lista_chamada.unidade_saude.nome,
                        atendimento.lista_chamada.get_situacao_display(),
                        atendimento.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        data_inicial.strftime('%Y-%m-%d %H:%M:%S') if data_inicial else '',
                        data_final.strftime('%Y-%m-%d %H:%M:%S') if data_final else '',
                        unidade_saude if unidade_saude else '',
                    ])
                    total += 1

                writer.writerow(['', '', '', '', '', '', '', 'Total'])
                writer.writerow(['', '', '', '', '', '', '', total])
                
                messages.info(request, 'Relatório exportado com sucesso!')

                return response
        else:
            form = RelatorioAtendimentosForm()

        return render(request, 'admin/exportar_relatorio_atendimentos.html', {'form': form})

    def exportar_relatorio_button(self, obj):
        return format_html('<a class="button" href="{}">Exportar Relatório</a>', reverse('admin:exportar_relatorio_atendimentos'))

    exportar_relatorio_button.short_description = 'Exportar Relatório'
    exportar_relatorio_button.allow_tags = True

@admin.register(EvolucaoAtendimento)
class EvolucaoAtendimentoAdmin(admin.ModelAdmin):
    list_display= ('nome_paciente', 'atendimento', 'numero_evolucao', 'profissional', 'registro_evolucao')
    search_fields = ('atendimento__paciente__nome_paciente',)
    ordering = ["-created_at"]

    def nome_paciente(self, obj):
        if obj.atendimento.paciente:
            return obj.atendimento.paciente.nome_paciente
        return None

@admin.register(DiagnosticoAtendimento)
class DiagnosticoAtendimentoAdmin(admin.ModelAdmin):
    list_display= ('atendimento', 'cid', 'arquivo')
    search_fields = ('atendimento__paciente__nome_paciente',)
    ordering = ["-created_at"]

class ArquivoExameAtendimentoInline(admin.TabularInline):
    model = ArquivoExameAtendimento
    extra = 0
    show_change_link = True
    readonly_fields = ['exame_atendimento', 'arquivo', 'nome']
    ordering = ['-created_at']

@admin.register(ExameAtendimento)
class ExameAtendimentoAdmin(admin.ModelAdmin):
    list_display= ('nome_paciente', 'atendimento', 'exame', 'lista_chamada_solicitacao', 'situacao')
    readonly_fields = ['lista_chamada_solicitacao',]
    search_fields = ('atendimento__paciente__nome_paciente',)
    inlines = [ArquivoExameAtendimentoInline,]
    ordering = ["-created_at"]

    def nome_paciente(self, obj):
        if obj.atendimento.paciente:
            return obj.atendimento.paciente.nome_paciente
        return None

class ArquivoProcedimentoAtendimentoInline(admin.TabularInline):
    model = ArquivoProcedimentoAtendimento
    extra = 0
    show_change_link = True
    readonly_fields = ['procedimento_atendimento', 'arquivo', 'nome']
    ordering = ['-created_at']

@admin.register(ProcedimentoAtendimento)
class ProcedimentoAtendimentoAdmin(admin.ModelAdmin):
    list_display= ('nome_paciente', 'atendimento', 'procedimento', 'tipo_solicitacao', 'quantidade', 'situacao', 'created_at')
    search_fields = ('atendimento__paciente__nome_paciente',)
    inlines = [ArquivoProcedimentoAtendimentoInline,]
    ordering = ["-created_at"]

    def nome_paciente(self, obj):
        if obj.atendimento.paciente:
            return obj.atendimento.paciente.nome_paciente
        return None

class SituacaoMedicacaoAtendimentoInline(admin.TabularInline):
    model = SituacaoMedicacaoAtendimento
    extra = 0
    show_change_link = True
    readonly_fields = ['data_hora_aplicacao', 'medicacao_atendimento', 'enfermeiro']
    ordering = ['created_at']

@admin.register(MedicacaoAtendimento)
class MedicacaoAtendimentoAdmin(admin.ModelAdmin):
    list_display= ('atendimento', 'medico', 'situacao')
    readonly_fields = ['lista_chamada_solicitacao',]
    inlines = [SituacaoMedicacaoAtendimentoInline, ]	
    search_fields = ('atendimento__paciente__nome_paciente',)
    ordering = ["-created_at"]

@admin.register(AtestadoAtendimento)
class AtestadoAtendimentoAdmin(admin.ModelAdmin):
    list_display= ('atendimento', 'profissional')
    search_fields = ('atendimento__paciente__nome_paciente',)
    ordering = ["-created_at"]

@admin.register(FichaReferenciaAtendimento)
class FichaReferenciaAtendimentoAdmin(admin.ModelAdmin):
    list_display= ('nome_paciente', 'atendimento', 'profissional')
    readonly_fields = ['exames', 'medicacoes', 'diagnosticos']
    search_fields = ('atendimento__paciente__nome_paciente',)
    ordering = ["-created_at"]

    def nome_paciente(self, obj):
        if obj.atendimento.paciente:
            return obj.atendimento.paciente.nome_paciente
        return None

@admin.register(HorarioMedico)
class HorarioMedicoAdmin(admin.ModelAdmin):
    list_display= ('medico_horariomedico', 'dia_semana_horariomedico', 'hora_inicial_horariomedico')

@admin.register(AgendamentoConsultorio)
class AgendaMedicaAdmin(admin.ModelAdmin):
    list_display= ('paciente', 'nome_paciente', 'cpf_paciente')
    
@admin.register(Feriado)
class FeriadoAdmin(admin.ModelAdmin):
    list_display= ('nome_feriado', 'data_inicial', 'data_final')

@admin.register(BloqueioAgenda)
class BloqueioAgendaAdmin(admin.ModelAdmin):
    list_display= ('medico_bloqueio_agenda', 'data_inicial', 'data_final')

@admin.register(JustificativaProcedimentoAtendimento)
class JustificativaProcedimentoAtendimentoAdmin(admin.ModelAdmin):
    list_display= ('id', 'atendimento')