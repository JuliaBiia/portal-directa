from django.utils import timezone
from rest_framework import serializers
from datetime import datetime, timedelta

from publicmanager.saude_enfermagem import utils 
from publicmanager.saude_enfermagem.models import (
    ListaChamadaSolicitacaoAtendimento, SolicitacaoAtendimento, SituacaoMedicacaoAtendimento, RequisicaoSolicitacaoAtendimento,
    ReceitaMedicamento, AdministracaoMedicamento, SituacaoAdministracaoMedicamento, SituacaoAdministracaoMedicamento, ListaChamadoAdministracaoMedicamento,
    AdministracaoProcedimento, SituacaoAdministracaoProcedimento
)
from publicmanager.saude_atendimento.models import MedicacaoAtendimento, ExameAtendimento, ProcedimentoAtendimento, ArquivoExameAtendimento

class ChamadoSolicitacaoUpdateSerializer(serializers.ModelSerializer):
        class Meta:
                model = ListaChamadaSolicitacaoAtendimento
                fields = ('contagem', 'updated_at')

class SituacaoMedicacaoAtendimentoSerializer(serializers.ModelSerializer):
        posologia = serializers.SerializerMethodField()
        class Meta:
                model = SituacaoMedicacaoAtendimento
                fields = ('medicacao_atendimento', 'enfermeiro', 'data_hora_aplicacao', 'posologia', 'created_at')

        def get_posologia(self, obj):
                return obj.medicacao_atendimento.posologia

class AdministacaoMedicacaoSerializer(serializers.ModelSerializer):
        medicamento_nome = serializers.SerializerMethodField()
        admin_medicamentosa_nome = serializers.SerializerMethodField()
        medico_nome = serializers.SerializerMethodField()
        medicacao = serializers.SerializerMethodField()
        paciente_nome = serializers.SerializerMethodField()
        medico = serializers.SerializerMethodField()
        tipo_parenteral_nome = serializers.SerializerMethodField()
        situacao_medicacao = serializers.SerializerMethodField()
        proxima_aplicacao = serializers.SerializerMethodField()
        contagem_aplicacoes = serializers.SerializerMethodField()
        tipo_posologia = serializers.SerializerMethodField()
        
        class Meta:
                model = MedicacaoAtendimento
                fields = (
                        'id', 
                        'medicamento_nome', 
                        'dosagem', 
                        'posologia', 
                        'admin_medicamentosa_nome', 
                        'medico_nome',
                        'posologia',
                        'tipo_parenteral',
                        'admin_medicamentosa',
                        'duracao_tratamento',
                        'uso_continuo',
                        'observacao',
                        'medicacao',
                        'paciente_nome',
                        'medico',
                        'tipo_parenteral_nome',
                        'situacao',
                        'contagem_aplicacoes',
                        'situacao_medicacao',
                        'proxima_aplicacao',
                        'tipo_posologia',
                        'dose_unica'
                )

        def get_medicamento_nome(self, obj):
                return obj.medicacao.nome_medicamento
        
        def get_admin_medicamentosa_nome(self, obj):
                return obj.get_admin_medicamentosa_display()
        
        def get_medico_nome(self, obj):
                return obj.medico.nome_profissional
        
        def get_medicacao(self, obj):
                return {'id': obj.medicacao.id, 'text': obj.medicacao.nome_medicamento}
        
        def get_paciente_nome(self, obj):
                return obj.atendimento.paciente.nome_paciente
        
        def get_medico(self, obj):
                return {'id': obj.medico.id, 'nome': obj.medico.nome_profissional } if obj.medico else {'id': None, 'nome': None }
        
        def get_tipo_parenteral_nome(self, obj):
                return obj.get_tipo_parenteral_display()
        
        def get_contagem_aplicacoes(self, obj):
                return SituacaoMedicacaoAtendimento.objects.filter(medicacao_atendimento=obj.pk, data_hora_aplicacao__isnull=False, cancelado=False).count()
        
        def get_situacao_medicacao(self, obj):
                situacaoes = SituacaoMedicacaoAtendimento.objects.filter(medicacao_atendimento=obj.pk, data_hora_aplicacao__isnull=False, cancelado=False).order_by('data_hora_aplicacao')
                return SituacaoMedicacaoAtendimentoSerializer(instance=situacaoes, many=True).data
        
        def get_proxima_aplicacao(self, obj):
                return obj.calcular_proxima_dosagem()
        
        def get_tipo_posologia(self, obj):
                return obj.get_tipo_posologia_display()

class AtualizarAplicacaoSerializer(serializers.ModelSerializer):

        class Meta:
                model = MedicacaoAtendimento
                fields = ('id', 'situacao')

class MedicacaoTimeLineSerializer(serializers.ModelSerializer):
        nome = serializers.SerializerMethodField()
        admin_medicamentosa = serializers.SerializerMethodField()
        class Meta:
                model = MedicacaoAtendimento
                fields = ('nome', 'dosagem', 'admin_medicamentosa', 'posologia', 'duracao_tratamento', 'observacao', 'tipo_parenteral')

        def get_nome(self, obj):
                return obj.medicacao.nome_medicamento
        
        def get_admin_medicamentosa(self, obj):
                return obj.get_admin_medicamentosa_display()
        
class ExameAtendimentoSerializer(serializers.ModelSerializer):
        nome = serializers.SerializerMethodField()
        tipo_exame = serializers.SerializerMethodField()
        medico_solicitante = serializers.SerializerMethodField()
        arquivos = serializers.SerializerMethodField()
        class Meta:
                model = ExameAtendimento
                fields = ('id',
                        'nome',
                        'atendimento',
                        'medico_solicitante',
                        'profissional_responsavel',
                        'exame',
                        'situacao',
                        'observacao',
                        'arquivo',
                        'justificativa',
                        'arquivo_nome',
                        'tipo_exame',
                        'arquivos'
                )

        def get_nome(self, obj):
                return obj.exame.nome
        
        def get_tipo_exame(self, obj):
                return obj.exame.tipo_exame.nome
        
        def get_medico_solicitante(self, obj):
                return {'id': obj.medico_solicitante.id, 'nome': obj.medico_solicitante.nome_profissional } if obj.medico_solicitante else {'id': None, 'nome': None }
        
        def get_arquivos(self, obj):
                arquivo = ArquivoExameAtendimento.objects.filter(exame_atendimento=obj).values('id', 'arquivo', 'nome')
                return arquivo

class ProcedimentosAtendimentoSerializer(serializers.ModelSerializer):
        nome = serializers.SerializerMethodField()
        medico_solicitante = serializers.SerializerMethodField()
        class Meta:
                model = ProcedimentoAtendimento
                fields = ('id',
                        'nome',
                        'procedimento',
                        'quantidade',
                        'arquivo',
                        'situacao',
                        'arquivo_nome',
                        'classificacao',
                        'medico_solicitante'
                )

        def get_nome(self, obj):
                return obj.procedimento.nome
        
        def get_medico_solicitante(self, obj):
                return {'id': obj.medico_solicitante.id, 'nome': obj.medico_solicitante.nome_profissional } if obj.medico_solicitante else {'id': None, 'nome': None }

class SolicitacoesTimeLineSerializer(serializers.ModelSerializer):
        profissional_nome = serializers.SerializerMethodField()
        numero_atendimento = serializers.SerializerMethodField()
        data_entrada = serializers.SerializerMethodField()
        alergias_medicamentosas = serializers.SerializerMethodField()
        timeline_solicitacoes = serializers.SerializerMethodField()
        progresso = serializers.SerializerMethodField()
        class Meta:
                model = RequisicaoSolicitacaoAtendimento
                fields = '__all__'

        def get_profissional_nome(self, obj):
                return obj.atendimento.profissionais.first().nome_profissional
        
        def get_numero_atendimento(self, obj):
                return obj.atendimento.lista_chamada.classificacao_risco.formatar_numeros_atendimento
        
        def get_data_entrada(self, obj):
                return timezone.localtime(obj.atendimento.lista_chamada.classificacao_risco.boletim.created_at).strftime('%d/%m/%Y %H:%m')
        
        def get_alergias_medicamentosas(self, obj):
                if obj.atendimento.paciente.anamnese_paciente:
                        return obj.atendimento.paciente.anamnese_paciente.alergias_medicamentosas.all().values_list('nome', flat=True)
                
                return []
        
        def get_timeline_solicitacoes(self, obj):
                requisicao = RequisicaoSolicitacaoAtendimento.objects.filter(pk=obj.pk).order_by('created_at').first()
                lista_chamadas = requisicao.listas_chamadas_solicitacoes.order_by('sequencial')

                tipos_solicitacoes = [
                        {'tipo': ListaChamadaSolicitacaoAtendimento.EXAME_LABORATORIO},
                        {'tipo': ListaChamadaSolicitacaoAtendimento.EXAME_IMAGEM},
                        {'tipo': ListaChamadaSolicitacaoAtendimento.PROCEDIMENTO},
                        {'tipo': ListaChamadaSolicitacaoAtendimento.MEDICACAO},
                ]

                # Mapeando sequenciais para cada tipo de solicitação
                for solicitacao in tipos_solicitacoes:
                        instancia_ordenacao = lista_chamadas.filter(tipo=solicitacao['tipo']).order_by('-created_at').first()
                        
                        if instancia_ordenacao:
                                solicitacao['id'] = instancia_ordenacao.id
                                solicitacao['sequencial'] = instancia_ordenacao.sequencial

                # Ordenando tipos de solicitação por sequencial
                tipos_solicitacoes_ordenados = sorted(tipos_solicitacoes, key=lambda x: x.get('sequencial', float('inf')))

                medicacoes_list = None
                timeline_list = []
                for (index, tipo_solicitacao) in enumerate(tipos_solicitacoes_ordenados):

                        solicitacao = SolicitacaoAtendimento.objects.filter(
                                lista_chamada_solicitacao__in=lista_chamadas,
                                lista_chamada_solicitacao__tipo=tipo_solicitacao['tipo']
                        ).order_by('-created_at').first()
                

                        if solicitacao:
                                medicacoes = MedicacaoAtendimento.objects.filter(lista_chamada_solicitacao=solicitacao.lista_chamada_solicitacao, aplicacao=MedicacaoAtendimento.IMEDIATA)

                                if medicacoes:
                                        medicacoes_list = MedicacaoTimeLineSerializer(instance=medicacoes, many=True).data
                                        
                                enfermeiro = solicitacao.enfermeiros.first()
                                enfermeiro_serializable = {'id': enfermeiro.id, 'nome': enfermeiro.nome_profissional}
                                timeline_list.append({
                                        'line': True,
                                        'tipo': solicitacao.lista_chamada_solicitacao.tipo,
                                        'sequencial': solicitacao.lista_chamada_solicitacao.sequencial,
                                        'numero': solicitacao.numero_solicitacao_formatado,
                                        'responsavel': enfermeiro_serializable,
                                        'data_entrada': timezone.localtime(solicitacao.created_at).strftime('%d/%m/%Y %H:%M'),
                                        'situacao': solicitacao.lista_chamada_solicitacao.situacao,
                                })
                        else:
                                if tipo_solicitacao['tipo'] == ListaChamadaSolicitacaoAtendimento.EXAME_LABORATORIO:
                                        solicitado = lista_chamadas.filter(tipo=ListaChamadaSolicitacaoAtendimento.EXAME_LABORATORIO).exists()
                                        tipo = 0
                                elif tipo_solicitacao['tipo'] == ListaChamadaSolicitacaoAtendimento.EXAME_IMAGEM:
                                        solicitado = lista_chamadas.filter(tipo=ListaChamadaSolicitacaoAtendimento.EXAME_IMAGEM).exists()
                                        tipo = 1
                                elif tipo_solicitacao['tipo'] == ListaChamadaSolicitacaoAtendimento.PROCEDIMENTO:
                                        solicitado = lista_chamadas.filter(tipo=ListaChamadaSolicitacaoAtendimento.PROCEDIMENTO).exists()
                                        tipo = 2
                                elif tipo_solicitacao['tipo'] == ListaChamadaSolicitacaoAtendimento.MEDICACAO:
                                        solicitado = lista_chamadas.filter(tipo=ListaChamadaSolicitacaoAtendimento.MEDICACAO).exists()
                                        tipo = 3

                                timeline_list.append({'line': False, 'tipo': tipo, 'processo': solicitado, 'sequencial': index + 1})

                return {'timeline_list': timeline_list, 'medicacoes': medicacoes_list}
        
        def get_progresso(self, obj):
                requisicao = obj.listas_chamadas_solicitacoes.filter(
                        situacao__in=[ListaChamadaSolicitacaoAtendimento.EM_ESPERA,
                                ListaChamadaSolicitacaoAtendimento.EM_ATENDIMENTO,
                                ListaChamadaSolicitacaoAtendimento.DESIGNADO
                        ]).first()
                return requisicao.sequencial if requisicao else None  
        
class AdministracaoMedicamentoListagemSerializer(serializers.ModelSerializer):
        medicacao_nome = serializers.SerializerMethodField()
        quantidade_aplicado = serializers.SerializerMethodField()
        admin_medicamentosa_nome = serializers.SerializerMethodField()
        tipo_parenteral_nome = serializers.SerializerMethodField()
        periodo_nome = serializers.SerializerMethodField()
        aplicados = serializers.SerializerMethodField()
        cancelados = serializers.SerializerMethodField()
        em_aberto = serializers.SerializerMethodField()
        class Meta:
                model = AdministracaoMedicamento
                fields = '__all__'

        def get_medicacao_nome(self, obj):
                return obj.medicacao.nome_medicamento
        
        def get_quantidade_aplicado(self, obj):
                return SituacaoAdministracaoMedicamento.objects.filter(administracao_medicamento__id=obj.id).count()
        
        def get_admin_medicamentosa_nome(self, obj):
                return obj.get_admin_medicamentosa_display()
        
        def get_tipo_parenteral_nome(self, obj):
                return obj.get_tipo_parenteral_display()
        
        def get_periodo_nome(self, obj):
                return obj.get_periodo_display()
        
        def get_aplicados(self, obj):
                return SituacaoAdministracaoMedicamento.objects.filter(administracao_medicamento__id=obj.id, situacao=SituacaoAdministracaoMedicamento.APLICADO).count()
        
        def get_cancelados(self, obj):
                return SituacaoAdministracaoMedicamento.objects.filter(administracao_medicamento__id=obj.id, situacao=SituacaoAdministracaoMedicamento.CANCELADO).count()

        def get_em_aberto(self, obj):
                return SituacaoAdministracaoMedicamento.objects.filter(administracao_medicamento__id=obj.id, situacao=SituacaoAdministracaoMedicamento.SOLICITADO).count()

class ReceitaMedicamentoSerializer(serializers.ModelSerializer):
        data_entrada = serializers.SerializerMethodField()
        paciente_nome = serializers.SerializerMethodField()
        paciente_cartao_sus = serializers.SerializerMethodField()
        administracao_medicamento_listagem = serializers.SerializerMethodField()
        tipo = serializers.SerializerMethodField()

        class Meta:
                model = ReceitaMedicamento
                fields = '__all__'

        def get_paciente_nome(self, obj):
                return obj.paciente.nome_paciente
        
        def get_paciente_cartao_sus(self, obj):
                return obj.paciente.cartao_sus
        
        def get_tipo(self, obj):
                return obj.lista_chamada_solicitacao.boletim.get_tipo_display()
        
        def get_data_entrada(self, obj):
                return obj.lista_chamada_solicitacao.boletim.created_at.strftime("%d/%m/%Y %H:%M")
        
        def get_administracao_medicamento_listagem(self, obj):
                administracao_medicamentos = AdministracaoMedicamento.objects.filter(receita_medicamento__id=obj.id)
                return AdministracaoMedicamentoListagemSerializer(administracao_medicamentos, many=True).data
        
class SituacaoAdministracaoMedicamentoSerializer(serializers.ModelSerializer):
        enfermeiro_nome = serializers.SerializerMethodField()
        data_hora_aplicacao = serializers.SerializerMethodField()
        proxima_hora_aplicacao = serializers.SerializerMethodField()

        class Meta:
                model = SituacaoAdministracaoMedicamento
                fields = '__all__'

        def get_enfermeiro_nome(self, obj):
                if obj.enfermeiro:
                        return obj.enfermeiro.nome_profissional
                return None

        def get_data_hora_aplicacao(self, obj):
                if obj.data_hora_aplicacao:
                        return obj.data_hora_aplicacao.strftime('%d/%m/%Y %H:%m')
                return None
        
        def get_proxima_hora_aplicacao(self, obj):
                ultima_aplicacao = SituacaoAdministracaoMedicamento.objects.filter(
                        administracao_medicamento__id=obj.administracao_medicamento.id,
                        situacao__in=[SituacaoAdministracaoMedicamento.APLICADO, SituacaoAdministracaoMedicamento.CANCELADO]
                ).order_by('-data_hora_aplicacao').first()

                if ultima_aplicacao and ultima_aplicacao.data_hora_aplicacao:

                        if isinstance(ultima_aplicacao.data_hora_aplicacao, datetime):
                                data_ultima_aplicacao_str = ultima_aplicacao.data_hora_aplicacao.strftime('%d/%m/%Y %H:%M')
                        else:
                                data_ultima_aplicacao_str = ultima_aplicacao.data_hora_aplicacao

                        periodo = obj.administracao_medicamento.periodo

                        if periodo == AdministracaoMedicamento.DIARIA:
                                posologia = obj.administracao_medicamento.posologia
                                
                                return {
                                        'proximo': utils.calcular_proxima_hora_aplicacao_diaria(data_ultima_aplicacao_str, posologia),
                                        'ultimo_sequencial': ultima_aplicacao.sequencial
                                }
                        elif periodo == AdministracaoMedicamento.SEMANAL:
                                return {
                                        'proximo': utils.calcular_proxima_hora_aplicacao_semanal(data_ultima_aplicacao_str),
                                        'ultimo_sequencial': ultima_aplicacao.sequencial
                                }
                        elif periodo == AdministracaoMedicamento.MENSAL:
                                return {
                                        'proximo': utils.calcular_proxima_hora_aplicacao_mensal(data_ultima_aplicacao_str),
                                        'ultimo_sequencial': ultima_aplicacao.sequencial
                                }

                return {
                        'proximo': None,
                        'ultimo_sequencial': None
                }
                
class ListaChamadoAdministracaoMedicamentoSerializer(serializers.ModelSerializer):
        class Meta:
                model = ListaChamadoAdministracaoMedicamento
                fields = '__all__'

class SolicitacaoAdministracaoProcedimentoSerializer(serializers.ModelSerializer):
        id_procedimento = serializers.CharField(source="procedimento.id", read_only=True)
        nome_procedimento = serializers.CharField(source="procedimento.nome", read_only=True)
        situacao_procedimento = serializers.SerializerMethodField()

        class Meta:
                model = AdministracaoProcedimento
                fields = '__all__'

        def get_situacao_procedimento(self, obj):
                situacao = SituacaoAdministracaoProcedimento.objects.filter(
                        administracao_procedimento=obj.pk
                ).order_by('data_hora_execucao').first()

                return situacao.situacao if situacao else 0

class SituacaoAdministracaoProcedimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SituacaoAdministracaoProcedimento
        fields = '__all__'