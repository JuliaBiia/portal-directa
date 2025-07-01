from django.urls import path, include
from rest_framework.routers import DefaultRouter
from publicmanager.saude_atendimento.views import (
    urgencia as views_urgencia, consultorio as views_consultorio, atendimento as views_atendimento
)
from publicmanager.saude_atendimento.api.views import urgencia as api_urgencia, consultorio as api_consultorio, atendimento as api_atendimento

saude_atendimento_router = DefaultRouter()
saude_atendimento_router.register('atendimento', api_urgencia.AtendimentoMedicoViewSet, basename='atendimentos')

app_name = 'saude_atendimento'

urlpatterns = [
    ## Adimissão de Paciente
    path('pacientes/admissao/', views_atendimento.AdmissaoPacienteListView.as_view(), name='admissao_paciente_list'),
    path('paciente/admissao/criar/', views_atendimento.AdmissaoPacienteCreateView.as_view(), name='admissao_paciente_add'),
    path('paciente/admissao/<uuid:pk>/atualizar/', views_atendimento.AdmissaoPacienteUpdateView.as_view(), name='admissao_paciente_update'),
    path('paciente/admissao/<uuid:pk>/deletar/', views_atendimento.AdmissaoPacienteDeleteView.as_view(), name='admissao_paciente_delete'),
    path('paciente/admissao/<uuid:pk>/pdf/', views_atendimento.RelatorioPacientePDFView.as_view(), name='relatorio_paciente_pdf'),
    path('paciente/rastreamento/', views_atendimento.RastreamentoPacientesListView.as_view(), name='rastreamento_pacientes_list'),
    
    ## Historico Paciente
    path('paciente/historico-atendimento/<uuid:pk>/', views_atendimento.PacienteHistoricoListView.as_view(), name='paciente_historico_list'),
    path('paciente/historico-time-line/<uuid:pk>/', views_atendimento.PacienteHistoricoTimeLineListView.as_view(), name='paciente_historico_time_line'),
    path('paciente/historico-time-ficha/<uuid:pk>/', views_atendimento.PacienteHistoricoFichaListView.as_view(), name='paciente_historico_ficha'),

    # Atendimentos Finalizados
    path('pacientes/atendimentos-finalizados/', views_urgencia.AtendimentoFinalizadoListView.as_view(), name='atendimentos_finalizados_list'),
    
    ## Novo Boletim
    path('paciente/novoboletim/criar/', views_urgencia.PacienteNovoBoletimCreateView.as_view(), name='add_boletim'),
    path('paciente/novoboletim/<uuid:pk>/', views_urgencia.PacienteNovoBoletimDetailView.as_view(), name='paciente_boletim_listagem'),
    path('paciente/novoboletim/<uuid:pk>/atualizar/', views_urgencia.PacienteNovoBoletimUpdateView.as_view(), name='novo_boletim_update'),
    path('paciente/novoboletim/<uuid:pk>/deletar/', views_urgencia.PacienteNovoBoletimDeleteView.as_view(), name='paciente_boletim_delete'),

    ## Classificação de risco
    path('pacientes/classificacao-risco/', views_urgencia.ClassificacaoRiscoListView.as_view(), name='classificacao_risco_list'),
    path('paciente/classificacao-risco/<uuid:pk>/criar/', views_urgencia.ClassificacaoRiscoCreateView.as_view(), name='classificacao_risco_create'),
    path('paciente/classificacao-risco/<uuid:pk>/atualizar/', views_urgencia.ClassificacaoRiscoUpdateView.as_view(), name='classificacao_risco_update'),
    path('paciente/classificacao-risco/<uuid:pk>/pdf/', views_urgencia.RelatorioClassificacaoPacientePDFView.as_view(), name='relatorio_classificacao_paciente_pdf'),
    path('paciente/classificacao-risco/<uuid:boletim_id>/', views_urgencia.ListaChamadaClassificacaoRiscoCreateView.as_view(), name='lista_chamada_classificacao_risco_create'),

    ## Pacientes aguardando ou em atendimento
    path('pacientes/aguardando-atendimento/', views_urgencia.PacientesAguardandoAtendimentoListView.as_view(), name='pacientes_aguardando_atendimento_list'),
    path('paciente/atendimento/<uuid:pk>/pdf/', views_urgencia.RelatorioPacienteAtendimentoPDFView.as_view(), name='relatorio_paciente_atendimento_pdf'),

    ## Anamnese
    path('anamnese/criar/', views_atendimento.AnamnesePacienteCreateView.as_view(), name='anamnese_add'),
    path('anamnese/<uuid:pk>/atualizar/', views_atendimento.AnamnesePacienteUpdateView.as_view(), name='anamnese_update'),
    
    ## Atendimento Medico
    path('paciente/atendimento-medico/', views_urgencia.AtendimentoMedicoListView.as_view(), name='atendimento_medico_list'),
    path('paciente/atendimento-medico/<uuid:pk>/detalhes/', views_urgencia.AtendimentoMedicoDetailView.as_view(), name='atendimento_medico_detail'),
    path('paciente/atendimento-medico/medicacao-posterior/<uuid:pk>/pdf/', views_urgencia.AtendimentoMedicacaoPosteriorPdfView.as_view(), name='relatorio_medicacao_posterior_pdf'),
    path('paciente/atendimento-medico/declaracao-acompanhante/<uuid:pk>/pdf/', views_urgencia.DeclaracaoAcompanhantePdfView.as_view(), name='relatorio_paciente_declaracao_pdf'),
    path('paciente/atendimento-medico/declaracao-comparacimento/<uuid:pk>/pdf/', views_urgencia.DeclaracaoConsultaExamePdfView.as_view(), name='relatorio_paciente_comparecimento_pdf'),
    path('paciente/atendimento-medico/receita-medica/<uuid:pk>/pdf/', views_urgencia.ReceitaPosteriorImediataPdfView.as_view(), name='receita_posterior_imediata_pdf'),
    path('paciente/atendimento-medico/atestado-medico/', views_urgencia.AtendimentoAtestadoListView.as_view(), name='atendimento_atestado_list'),
    path('paciente/atendimento-medico/atestado-medico/criar/', views_urgencia.AtendimentoAtestadoCreateView.as_view(), name='atendimento_atestado_create'),
    path('paciente/atendimento-medico/atestado-medico/<uuid:pk>/pdf/', views_urgencia.AtendimentoAtestadoPdfView.as_view(), name='atendimento_atestado_pdf'),
    path('paciente/atendimento-medico/ficha-referencia/listagem/', views_urgencia.AtendimentoFichaReferenciaListView.as_view(), name='atendimento_ficha_list'),
    path('paciente/atendimento-medico/ficha-referencia/<uuid:pk>/criar/', views_urgencia.AtendimentoFichaReferenciaCreateView.as_view(), name='atendimento_ficha_referencia_create'),
    path('paciente/atendimento-medico/ficha-referencia/<uuid:pk>/pdf/', views_urgencia.AtendimentoFichaReferenciaPdfView.as_view(), name='relatorio_ficha_referencia_pdf'),
    
    ## Justificativa Procedimento
    path('justificativa-procedimento/', views_urgencia.JustificativaProcedimentoAtendimentoCreateView.as_view(), name='justificativa_procedimento_atendimento_create'),
    path('justificativa-procedimento/<uuid:pk>/atualizar/', views_urgencia.JustificativaProcedimentoAtendimentoUpdateView.as_view(), name='justificativa_procedimento_atendimento_update'),

    ## Lista de Chamados
    path('paciente/atendimento-medico/<uuid:id_paciente>/<uuid:id_boletim>/', views_urgencia.ListaChamadaCreateView.as_view(), name='lista_chamada_create'),
   
    ## Encaminhamento
    path('pacientes/encaminhamento/', views_urgencia.EncaminhamentoListView.as_view(), name='encaminhamento_list'),

    ## Concessão de Alta
    path('pacientes/concessao-de-alta/', views_urgencia.ConcessaoDeAltaListView.as_view(), name='concessao_alta_list'),

    ## Tipo de Alta Hospitalar
    path('tipo-alta-hospitalar/', views_urgencia.TipoAltaHospitalarListView.as_view(), name='tipoaltahospitalar_list'),
    path('tipo-alta-hospitalar/criar/', views_urgencia.TipoAltaHospitalarCreateView.as_view(), name='tipoaltahospitalar_add'),
    path('tipo-alta-hospitalar/<uuid:pk>/atualizar/', views_urgencia.TipoAltaHospitalarUpdateView.as_view(), name='tipoaltahospitalar_update'),
    path('tipo-alta-hospitalar/<uuid:pk>/deletar/', views_urgencia.TipoAltaHospitalarDeleteView.as_view(), name='tipoaltahospitalar_delete'),

    ## Atendimentos em aberto
    path('atendimentos-abertos/', views_urgencia.AtendimentosEmAbertoListView.as_view(), name='atendimentos_em_aberto_list'),
    path('atendimento/procedimentos/<uuid:pk>/relatorio/', views_urgencia.RelatorioProcedimentoSolicitacaoPDFView.as_view(), name='atendimento_procedimentos_relatorio'),
    
    ## Consultório
    ## Horário Médico
    path('horariomedico/', views_consultorio.HorarioMedicoView.as_view(), name='horario_medico_view'),
    path('horariomedico/<pk>/atualizar/', views_consultorio.HorarioMedicoUpdateView.as_view(), name='horario_medico_update'),
    path('horariomedico/<pk>/deletar/', views_consultorio.HorarioMedicoDeleteView.as_view(), name='horario_medico_delete'),

    ## Agenda Médica
    path('agendamedica/', views_consultorio.AgendaMedicaView.as_view(), name='agenda_medica_view'),
    path('agendamedica/medico/<uuid:medico_id>', views_consultorio.AgendaMedicaView.as_view(), name='agenda_medica_medico_view'),
    path('agendamedica/update_feriado_bloqueio_agenda/<str:alvoupdate>/<int:id>', views_consultorio.AgendaMedicaView.as_view(), name='update_feriado_bloqueio_agenda_view'),
    path('relatorio_agendamento/', views_consultorio.pdf_relatorio_agendamento, name='pdf_relatorio_agendamento'),
    path('relatorio_bloqueios_agenda/', views_consultorio.pdf_relatorio_bloqueios_agenda, name='pdf_relatorio_bloqueios_agenda'),
    path('agendamedica/busca/', views_consultorio.BuscarAgendamentosView.as_view(), name='buscar_agendamentos_view'),
    path('agendamedica/<uuid:pk>/deletar/', views_consultorio.AgendamentoConsultorioDeleteView.as_view(), name='agendamedica_delete'),

    ## Minha Agenda Médica
    path('minhaagendamedica/', views_consultorio.MinhaAgendaMedicaView.as_view(), name="minha_agenda_medica"),

    ## Pré-Atendimento
    path('paciente/preatendimento/<uuid:pk>/', views_consultorio.PreAtendimentoMedicoDetailView.as_view(), name='pre_atendimento_listagem'),
    path('paciente/preatendimento/criar/', views_consultorio.PreAtendimentoMedicoCreateView.as_view(), name='add_pre_atendimento'),
    path('paciente/preatendimento/<uuid:pk>/atualizar/', views_consultorio.PreAtendimentoMedicoUpdateView.as_view(), name='pre_atendimento_update'),
    path('paciente/preatendimento/<uuid:pk>/deletar/', views_consultorio.PreAtendimentoMedicoDeleteView.as_view(), name='pre_atendimento_delete'),

    # API
    path('api/pacientes/', api_urgencia.PacienteListAPIView.as_view(), name='pacienteapi_list'),
    path('api/paciente/detalhe/', api_urgencia.PacienteDetalheAPIView.as_view(), name='agendaapi_detalhe'),
    path('api/atualizar-chamado/<uuid:pk>/', api_urgencia.AtualizarChamadoUpdateAPIView.as_view(), name='api_atualizar_chamado'),
    path('api/finalizar-boletim/<uuid:pk>/', api_urgencia.FinalizarBoletimAtendimentoUpdateAPIView.as_view(), name='api_finalizar_boletim'),
    path('api/rastreamento/pacientes/', api_atendimento.RastrearPacientesAPIView.as_view(), name='api_rastrear_pacientes'),

    ## API - Atualizar Retorno Medicação
    path('api/atendimento/retorno-boletim-medicacao/<uuid:pk>/', api_urgencia.AtendimentoRetornoBoletimMedicacaoUpdateAPIView.as_view(), name='api_atendimento_retorno_boletim_medicacao_update'),

    ## API  - Cassificação Risco
    path('api/classificacao/atualizar-chamado/<uuid:pk>/', api_urgencia.AtualizarChamadoClassificacaoUpdateAPIView.as_view(), name='api_atualizar_classificacao_risco_chamado'),

    ## API - Consultório
    path('api/agendamedica/agendamentos/', api_consultorio.AgendamentoConsultorioListAPIView.as_view(), name='api_agendamento_list'),
    path('api/agendamedica/agendamento/criar/', api_consultorio.AgendamentoConsultorioAPICreateView.as_view(), name='api_agendamento_add'),

    path('api/agendamedica/agendamento/<int:id>/', api_consultorio.DetalheAgendamentoConsultorioAPIView.as_view(), name='api_detalhe_agendamento'),
    path('api/agendamedica/obterqtdatendimentodomedicoportipo/', api_consultorio.ObterQuantidadeDeAtendimentosDoMedicoPorTipoEmDeterminadaData.as_view(), name='api_obter_quantidade_de_atendimentos_do_medico_por_tipo_em_determinada_data'),
    path('api/agendamedica/buscarporperiododetempo/', api_consultorio.ObterAgendamentoPorDataInicialDataFinal.as_view(), name='api_obter_agendamento_por_data_inicial_data_final'),
    
    path('api/agendamedica/feriado/criar/', api_consultorio.FeriadoCreateView.as_view(), name='api_feriado_add'),
    path('api/agendamedica/feriado/<int:id>/atualizar/', api_consultorio.FeriadoUpdateView.as_view(), name='api_feriado_update'),
    path('api/agendamedica/feriado/<int:id>/deletar/', api_consultorio.FeriadoDeleteView.as_view(), name='api_feriado_delete'),
    
    path('api/agendamedica/bloqueioagenda/criar/', api_consultorio.BloqueioAgendaCreateView.as_view(), name='api_bloqueio_agenda_add'),
    path('api/agendamedica/bloqueioagenda/<int:id>/atualizar/', api_consultorio.BloqueioAgendaUpdateView.as_view(), name='api_bloqueio_agenda_update'),
    path('api/agendamedica/bloqueioagenda/<int:id>/deletar/', api_consultorio.BloqueioAgendaDeleteView.as_view(), name='api_bloqueio_agenda_delete'),
    
    path('api/', include(saude_atendimento_router.urls)),

    # Admin Django
    path('exportar_atendimentos/', views_atendimento.exportar_relatorio_atendimentos, name='exportar_relatorio_atendimentos'),
]