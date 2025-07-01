from simple_history.admin import SimpleHistoryAdmin
from django.contrib import admin
from .models import (
    ListaChamadaSolicitacaoAtendimento, SolicitacaoAtendimento, RequisicaoSolicitacaoAtendimento, 
    HistoricoEsperaSolicitacoes, SituacaoMedicacaoAtendimento, ListaChamadoAdministracaoMedicamento,
    ReceitaMedicamento, AdministracaoMedicamento, SituacaoAdministracaoMedicamento, HistoricoListaChamadoAdministracaoMedicamento,
    ReaberturaSolicitacaoAtendimento, ListaChamadoAdministracaoProcedimento, HistoricoListaChamadoAdministracaoProcedimento, ReceitaAdministracaoProcedimento, AdministracaoProcedimento, SituacaoAdministracaoProcedimento
)

class HistoricoEsperaAtendimentoInline(admin.TabularInline):
    model = HistoricoEsperaSolicitacoes
    extra = 0
    show_change_link = True
    readonly_fields = ['situacao', 'tempo_espera']
    ordering = ['created_at']

class ReaberturaSolicitacaoAtendimentoInline(admin.TabularInline):
    model = ReaberturaSolicitacaoAtendimento
    extra = 0
    show_change_link = True
    readonly_fields = ['medico_solicitante', 'justificativa']
    ordering = ['created_at']
    
@admin.register(ListaChamadaSolicitacaoAtendimento)
class ListaChamadaSolicitacaoAtendimentoAdmin(SimpleHistoryAdmin):
    list_display= ('nome_paciente', 'sala', 'atendimento', 'contagem', 'situacao', 'tipo', 'sequencial')
    inlines = [ReaberturaSolicitacaoAtendimentoInline, HistoricoEsperaAtendimentoInline,]
    search_fields = ('atendimento__paciente__nome_paciente', 'enfermeiro__nome_profissional')

    def nome_paciente(self, obj):
        if obj.atendimento:
            return obj.atendimento.paciente.nome_paciente
        return None	
@admin.register(SolicitacaoAtendimento)
class SolicitacaoAtendimentoAdmin(admin.ModelAdmin):
    list_display= ('nome_paciente', 'lista_chamada_solicitacao', 'numero_atendimento', 'numero_solicitacao_formatado')
    readonly_fields = ['enfermeiros',]
    search_fields = ('lista_chamada_solicitacao__atendimento__paciente__nome_paciente',)

    def nome_paciente(self, obj):
        if obj.lista_chamada_solicitacao.atendimento.paciente:
            return obj.lista_chamada_solicitacao.atendimento.paciente.nome_paciente
        return None

@admin.register(RequisicaoSolicitacaoAtendimento)
class RequisicaoSolicitacaoAtendimentoAdmin(admin.ModelAdmin):
    list_display= ('nome_paciente', 'medico_solicitante', 'finalizado')
    search_fields = ('atendimento__paciente__nome_paciente',)

    def nome_paciente(self, obj):
        if obj.atendimento:
            return obj.atendimento.paciente.nome_paciente
        return None

@admin.register(SituacaoMedicacaoAtendimento)
class SituacaoMedicacaoAtendimentoAdmin(admin.ModelAdmin):
    list_display= ('nome_paciente', 'medicacao_atendimento', 'enfermeiro', 'data_hora_aplicacao')
    search_fields = ('enfermeiro__nome_profissional',)

    def nome_paciente(self, obj):
        if obj.medicacao_atendimento.atendimento.paciente:
            return obj.medicacao_atendimento.atendimento.paciente.nome_paciente
        return None

@admin.register(ListaChamadoAdministracaoMedicamento)
class ListaChamadoAdministracaoMedicamentoAdmin(admin.ModelAdmin):
    list_display= ('nome_paciente', 'boletim', 'unidade_saude', 'enfermeiro', 'situacao')
    search_fields = ('enfermeiro__nome_profissional',)

    def nome_paciente(self, obj):
        if obj.boletim.paciente:
            return obj.boletim.paciente.nome_paciente
        return None

@admin.register(ReceitaMedicamento)
class ReceitaMedicamento(admin.ModelAdmin):
    list_display= ('paciente', 'enfermeiro', 'lista_chamada_solicitacao')
    search_fields = ('paciente__nome_paciente',)
    
@admin.register(AdministracaoMedicamento)
class AdministracaoMedicamentoAdmin(admin.ModelAdmin):
    list_display= ('nome_paciente', 'receita_medicamento', 'medicacao')
    search_fields = ('receita_medicamento__paciente__nome_paciente',)

    def nome_paciente(self, obj):
        if obj.receita_medicamento:
            return obj.receita_medicamento.paciente.nome_paciente
        return None

@admin.register(SituacaoAdministracaoMedicamento)
class SituacaoAdministracaoMedicamentoAdmin(admin.ModelAdmin):
    list_display= ('sequencial', 'administracao_medicamento', 'enfermeiro', 'data_hora_aplicacao', 'situacao')

@admin.register(HistoricoListaChamadoAdministracaoMedicamento)
class HistoricoListaChamadoAdministracaoMedicamentoAdmin(admin.ModelAdmin):
    list_display= ('lista_chamado_administracao_medicamento', 'situacao', 'enfermeiro', 'tempo_espera')

@admin.register(ListaChamadoAdministracaoProcedimento)
class ListaChamadoAdministracaoProcedimentoAdmin(admin.ModelAdmin):
    list_display= ('classificacao_risco', 'unidade_saude', 'enfermeiro', 'situacao', 'contagem')

@admin.register(HistoricoListaChamadoAdministracaoProcedimento)
class HistoricoListaChamadoAdministracaoProcedimentoAdmin(admin.ModelAdmin):
    list_display= ('lista_chamado_administracao_procedimento', 'situacao', 'enfermeiro', 'tempo_espera')

@admin.register(ReceitaAdministracaoProcedimento)
class ReceitaAdministracaoProcedimentoAdmin(admin.ModelAdmin):
    list_display= ('paciente', 'enfermeiro', 'lista_chamada_solicitacao')

@admin.register(AdministracaoProcedimento)
class AdministracaoProcedimentoAdmin(admin.ModelAdmin):
    list_display = ('receita_procedimento', 'procedimento', 'quantidade')

@admin.register(SituacaoAdministracaoProcedimento)
class SituacaoAdministracaoProcedimentoAdmin(admin.ModelAdmin):
    list_display = ('sequencial', 'administracao_procedimento', 'enfermeiro', 'data_hora_execucao', 'situacao', 'cancelou')