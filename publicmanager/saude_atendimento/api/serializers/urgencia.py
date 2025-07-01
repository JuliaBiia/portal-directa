from django.db.models import F
from django.utils import timezone
from rest_framework import serializers

from publicmanager.saude_farmacia.models import Medicamento
from publicmanager.saude_cadastro.models import Exame, Profissional, TipoClassificacaoRisco
from publicmanager.saude_enfermagem.models import ListaChamadaSolicitacaoAtendimento, SituacaoMedicacaoAtendimento
from publicmanager.saude_atendimento.models import (
    Paciente, ListaChamada, ClassificacaoRisco, AtendimentoMedico, EvolucaoAtendimento, DiagnosticoAtendimento, ExameAtendimento,
    ProcedimentoAtendimento, AnamnesePaciente, DocumentoPaciente, BoletimPaciente, MedicacaoAtendimento, JustificativaProcedimentoAtendimento,
    ArquivoExameAtendimento
)

class PacienteSerializer(serializers.ModelSerializer):
        class Meta:
                model = Paciente
                fields = ('id','nome_paciente', 'cpf', 'telefone_fixo', 'celular')

class AtendimentoClassificacaoRiscoSerializer(serializers.ModelSerializer):
        tipo_classificacao_risco = serializers.SerializerMethodField()
        escala_dor_nome = serializers.SerializerMethodField()
        estado_geral_nome = serializers.SerializerMethodField()
        classificacoes_choice = serializers.SerializerMethodField()

        class Meta:
                model = ClassificacaoRisco
                fields = '__all__'

        def get_tipo_classificacao_risco(self, obj):
                return {'id': obj.tipo_classificacao_risco.id, 'nome': obj.tipo_classificacao_risco.get_tipo_display(), 'cor': obj.tipo_classificacao_risco.get_cor_display()}
        
        def get_escala_dor_nome(self, obj):
                if obj.escala_dor:
                        return obj.get_escala_dor_display()
                return None
        
        def get_estado_geral_nome(self, obj):
                return obj.get_estado_geral_display() if obj.estado_geral else None
        
        def get_classificacoes_choice(self, obj):
                tipos_risco = TipoClassificacaoRisco.objects.filter(unidade_saude=obj.boletim.unidade_saude)

                lista_tipos_riscos = []
                for tipo_risco in tipos_risco:
                        lista_tipos_riscos.append({'id': tipo_risco.id, 'tipo': tipo_risco.get_tipo_display(), 'cor': tipo_risco.get_cor_display()})
                
                return lista_tipos_riscos

class AtendimentoPacienteSerializer(serializers.ModelSerializer):
        prosissao_titulo = serializers.SerializerMethodField()
        raca_nome = serializers.SerializerMethodField()
        estado_civil_nome = serializers.SerializerMethodField()
        doador_sanguineo_nome = serializers.SerializerMethodField()
        doador_orgaos_nome = serializers.SerializerMethodField()
        municipio_nome = serializers.SerializerMethodField()
        uf = serializers.SerializerMethodField()
        class Meta:
                model = Paciente
                fields = '__all__'

        def get_prosissao_titulo(self, obj):
                return obj.profissao.titulo if obj.profissao else None

        def get_raca_nome(self, obj):
                return obj.get_raca_display() if obj.raca else None

        def get_estado_civil_nome(self, obj):
                return obj.get_estado_civil_display() if obj.estado_civil else None

        def get_doador_sanguineo_nome(self, obj):
                return obj.get_doador_sanguineo_display() if obj.doador_sanguineo else None

        def get_doador_orgaos_nome(self, obj):
                return obj.get_doador_de_orgaos_display() if obj.doador_de_orgaos else None
        
        def get_municipio_nome(self, obj):
                return obj.municipio.nome if obj.municipio else None
        
        def get_uf(self, obj):
                if obj.municipio and obj.municipio.estado:
                        return obj.municipio.estado.sigla
                return None
        
class ListagemHistoricoEvolucaoSerializer(serializers.ModelSerializer):
        numero_evolucao_formatado = serializers.SerializerMethodField()
        profissional = serializers.SerializerMethodField()
        paciente_nome = serializers.SerializerMethodField()
        class Meta:
                model = EvolucaoAtendimento
                fields = (
                        'id',
                        'paciente_nome',
                        'registro_evolucao',
                        'numero_evolucao_formatado',
                        'profissional',
                        'retorno',
                        'created_at'
                        )

        def get_numero_evolucao_formatado(self, obj):
                return obj.formatar_numero_evolucao 
        
        def get_profissional(self, obj):
                return {'id': obj.profissional.id, 'nome': obj.profissional.nome_profissional } if obj.profissional else {'id': None, 'nome': None }

        def get_paciente_nome(self, obj):
                return obj.atendimento.paciente.nome_paciente 

class ListagemHistoricoDiagnosticoSerializer(serializers.ModelSerializer):
        profissional = serializers.SerializerMethodField()
        numero_diagnostico_formatado = serializers.SerializerMethodField()
        arquivo_url = serializers.SerializerMethodField()
        cid_nome = serializers.SerializerMethodField()
        descricao = serializers.SerializerMethodField()
        paciente_nome = serializers.SerializerMethodField()
        class Meta:
                model = DiagnosticoAtendimento
                fields = (
                        'profissional', 
                        'descricao', 
                        'cid_nome', 
                        'nome_arquivo',
                        'arquivo_url', 
                        'numero_diagnostico_formatado',
                        'paciente_nome',
                )

        def get_profissional(self, obj):
                return {'id': obj.profissional.id, 'nome': obj.profissional.nome_profissional } if obj.profissional else {'id': None, 'nome': None }
        
        def get_numero_diagnostico_formatado(self, obj):
                return obj.formatar_numero_diagnostico
        
        def get_arquivo_url(self, obj):
                return obj.arquivo.url if obj.arquivo else None
        
        def get_cid_nome(self, obj):
                return obj.cid.nome if obj.cid else None
        
        def get_descricao(self, obj):
                return obj.descricao if obj.descricao else ''
                   
        def get_paciente_nome(self, obj):
                return obj.atendimento.paciente.nome_paciente 

class DocumentacaoPacienteSerializer(serializers.ModelSerializer):
        arquivo_url = serializers.SerializerMethodField()
        paciente_nome = serializers.SerializerMethodField()
        class Meta:
                model = DocumentoPaciente
                fields = '__all__'

        def get_arquivo_url(self, obj):
                return obj.arquivo.url if obj.arquivo else None
        
        def get_paciente_nome(self, obj):
                return obj.paciente.nome_paciente
        
class AtendimentoMedicoListSerializer(serializers.ModelSerializer):
        profissional = serializers.SerializerMethodField()
        profissional_coren = serializers.SerializerMethodField()
        numero_atendimento_formatado = serializers.SerializerMethodField()
        solicitacao_exames = serializers.SerializerMethodField()
        data_atual = serializers.SerializerMethodField()
        undade_nome = serializers.SerializerMethodField()
        atendimento_paciente = AtendimentoPacienteSerializer(source='paciente')
        classificacao = AtendimentoClassificacaoRiscoSerializer(source='lista_chamada.classificacao_risco')
        documentos = serializers.SerializerMethodField()
        evolucao = serializers.SerializerMethodField()
        diagnostico = serializers.SerializerMethodField()
        existe_solicitacoes_abertas = serializers.SerializerMethodField()
        sinais_vitais = serializers.SerializerMethodField()
        class Meta:
                model = AtendimentoMedico
                fields = '__all__'

        def get_profissional(self, obj):
               usuario = self.context['request'].user
               profissional = Profissional.objects.get(user=usuario)

               return {'id': profissional.id, 'nome':profissional.nome_profissional } if profissional else {'id': None, 'nome': None }
        
        def get_profissional_coren(self, obj):
                usuario = self.context['request'].user
                profissional = Profissional.objects.get(user=usuario)
                
                return profissional.coren if profissional else None

        def get_numero_atendimento_formatado(self, obj):
                if obj.lista_chamada.classificacao_risco:
                        return obj.lista_chamada.classificacao_risco.formatar_numeros_atendimento
                return None
        
        def get_solicitacao_exames(self, obj):
                return Exame.objects.filter().values('id', 'nome')
        
        def get_data_atual(self, obj):
                return timezone.now().date().strftime("%d/%m/%Y")
        
        def get_undade_nome(self, obj):
                return self.context['request'].user.profissional_set.first().unidadelogin.unidade.nome
        
        def get_sinais_vitais(self, obj):
                classificacao = ClassificacaoRisco.objects.filter(
                        id__in=obj.classificacao_risco.all().values_list('id', flat=True)
                ).annotate(profissional_coren=F('profissional__coren')).order_by('-created_at').values(
                        'created_at', 'presao_arterial', 'frequencia_cardiaca', 'frequencia_respiratoria', 
                        'temperatura', 'spo2', 'hgt', 'profissional_coren'
                ).order_by('-created_at')

                return classificacao
        
        def get_documentos(self, obj):
                documentos = DocumentoPaciente.objects.filter(paciente=obj.paciente.pk).order_by('-created_at')
                
                return DocumentacaoPacienteSerializer(instance=documentos, many=True).data
        
        def get_evolucao(self, obj):
                evolucoes = EvolucaoAtendimento.objects.filter(atendimento=obj.pk).order_by('-created_at')
                
                return ListagemHistoricoEvolucaoSerializer(instance=evolucoes, many=True).data
        
        def get_diagnostico(self, obj):
                diagnosticos = DiagnosticoAtendimento.objects.filter(atendimento=obj.pk).order_by('-created_at')
                
                return ListagemHistoricoDiagnosticoSerializer(instance=diagnosticos, many=True).data
        
        def get_existe_solicitacoes_abertas(self, obj):
                lista_chamado = ListaChamadaSolicitacaoAtendimento.objects.filter(atendimento=obj, 
                        situacao__in=[
                                ListaChamadaSolicitacaoAtendimento.SOLICITADO,
                                ListaChamadaSolicitacaoAtendimento.EM_ESPERA,
                                ListaChamadaSolicitacaoAtendimento.DESIGNADO,
                                ListaChamadaSolicitacaoAtendimento.EM_ATENDIMENTO,
                        ]
                ).exists()

                return lista_chamado

class AtualizarChamadoUpdateSerializer(serializers.ModelSerializer):
        class Meta:
                model = ListaChamada
                fields = ('contagem', 'updated_at')

class ListagemExamesSerializer(serializers.ModelSerializer):
        medico_solicitante = serializers.SerializerMethodField()
        nome = serializers.SerializerMethodField()
        tipo = serializers.SerializerMethodField()
        arquivos = serializers.SerializerMethodField()
        class Meta:
                model = ExameAtendimento
                fields = '__all__'

        def get_medico_solicitante(self, obj):
                return {'id': obj.medico_solicitante.id, 'nome': obj.medico_solicitante.nome_profissional } if obj.medico_solicitante else {'id': None, 'nome': None }
                
        def get_nome(self, obj):
                return obj.exame.nome
        
        def get_tipo(self, obj):
                return obj.exame.tipo_exame.tipo
        
        def get_arquivos(self, obj):
                arquivo = ArquivoExameAtendimento.objects.filter(exame_atendimento=obj).values('id', 'arquivo', 'nome')
                return arquivo
        
class ListagemProcedimentosSerializer(serializers.ModelSerializer):
        medico_solicitante = serializers.SerializerMethodField()
        procedimento_nome = serializers.SerializerMethodField()
        procedimento_codigo = serializers.SerializerMethodField()
        estabelecimento_solicitante = serializers.SerializerMethodField()
        procedimento_selecionado = serializers.SerializerMethodField()
        paciente_nome = serializers.SerializerMethodField()
        classificacao_nome = serializers.SerializerMethodField()
        realizado_por_nome = serializers.SerializerMethodField()
        class Meta:
                model = ProcedimentoAtendimento
                fields = (
                        'id',
                        'procedimento', 
                        'quantidade', 
                        'classificacao', 
                        'procedimento_nome',
                        'procedimento_codigo',
                        'estabelecimento_solicitante',
                        'arquivo',
                        'arquivo_nome',
                        'situacao',
                        'medico_solicitante',
                        'procedimento_selecionado',
                        'tipo_solicitacao',
                        'paciente_nome',
                        'classificacao_nome',
                        'lista_chamada_solicitacao',
                        'realizado_por',
                        'realizado_por_nome',
                )

        def get_procedimento_nome(self, obj):
                return obj.procedimento.nome
        
        def get_procedimento_codigo(self, obj):
                return obj.procedimento.codigo
        
        def get_estabelecimento_solicitante(self, obj):
                return obj.atendimento.unidade_saude.nome
        
        def get_medico_solicitante(self, obj):
                return {'id': obj.medico_solicitante.id, 'nome': obj.medico_solicitante.nome_profissional } if obj.medico_solicitante else {'id': None, 'nome': None }
        
        def get_procedimento_selecionado(self, obj):
                return { "value": obj.procedimento.id, "text": obj.procedimento.nome, "codigo": obj.procedimento.codigo }
        
        def get_paciente_nome(self, obj):
                return obj.atendimento.paciente.nome_paciente
        
        def get_classificacao_nome(self, obj):
                return obj.get_classificacao_display()
        
        def get_realizado_por_nome(self, obj):
                return obj.get_realizado_por_display()

class justificativaProcedimentosSerializer(serializers.ModelSerializer): 
        diagnostico_nome = serializers.SerializerMethodField()
        cid_principal_codigo = serializers.SerializerMethodField()
        cid_secundario_codigo = serializers.SerializerMethodField()
        cid_associada_codigo = serializers.SerializerMethodField() 
        class Meta:
                model = JustificativaProcedimentoAtendimento
                fields = '__all__'

        def get_diagnostico_nome(self, obj):
                return obj.diagnostico.nome if obj.diagnostico else None
        
        def get_cid_principal_codigo(self, obj):
                return obj.cid_10_principal.codigo if obj.cid_10_principal else None
        
        def get_cid_secundario_codigo(self, obj):
                return obj.cid_10_secundario.codigo if obj.cid_10_secundario else None
        
        def get_cid_associada_codigo(self, obj):
                return obj.cid_10_causa_associada.codigo if obj.cid_10_causa_associada else None
        
class ListagemAnamneseSerializer(serializers.ModelSerializer):
        alergias = serializers.SerializerMethodField()
        antecedentes_patologicos = serializers.SerializerMethodField()
        patologicos_familiares = serializers.SerializerMethodField()
        class Meta:
                model = AnamnesePaciente
                exclude = ['created_at', 'updated_at']

        def get_alergias(self, obj):
                return [{'value': alergia.id, 'text': alergia.nome} for alergia in obj.alergias_medicamentosas.all()]
        
        def get_antecedentes_patologicos(self, obj):
                return [{'value': pessoal.id, 'text': pessoal.nome, 'codigo': pessoal.codigo} for pessoal in obj.antecedentes_patologicos_pessoais.all()]
        
        def get_patologicos_familiares(self, obj):
                return [{'value': familiar.id, 'text': familiar.nome, 'codigo': familiar.codigo} for familiar in obj.antecedentes_patologicos_familiares.all()]

class AtualizarAnamneseSerializer(serializers.ModelSerializer):
        class Meta:
                model = AnamnesePaciente
                exclude = [
                        'id',
                        'antecedentes_patologicos_pessoais',
                        'antecedentes_patologicos_familiares',
                        'alergias_medicamentosas',
                ]

class HistoricoAnterioresSerializer(serializers.ModelSerializer):
        classificacao = serializers.SerializerMethodField()
        profissionais = serializers.SerializerMethodField()
        situacao_nome = serializers.SerializerMethodField()
        class Meta:
                model = BoletimPaciente
                fields = '__all__'

        def get_classificacao(self, obj):
                try:
                        classificacao_risco = ClassificacaoRisco.objects.filter(boletim=obj, status=ClassificacaoRisco.ATIVO).order_by('created_at').first()
                        if classificacao_risco:

                                return {'numero': classificacao_risco.formatar_numeros_atendimento,
                                        'queixa': classificacao_risco.queixa_principal,
                                        'tipo': classificacao_risco.tipo_classificacao_risco.tipo}
                        return ''
                
                except ClassificacaoRisco.DoesNotExist:
                        return ''
                
        def get_profissionais(self, obj):
                try:
                        atendimentos = AtendimentoMedico.objects.filter(lista_chamada__classificacao_risco__boletim=obj)
                        for atendimento in atendimentos:
                                nomes_profissionais = [profissional.nome_profissional for profissional in atendimento.profissionais.all()]

                                return nomes_profissionais
                        
                except AtendimentoMedico.DoesNotExist:
                        return ''
                
        def get_situacao_nome(self, obj):
                return obj.get_situacao_display()
        
class MedicacaoAtendimentoSerializer(serializers.ModelSerializer):
        medicamento_nome = serializers.SerializerMethodField()
        admin_medicamentosa_nome = serializers.SerializerMethodField()
        medico_nome = serializers.SerializerMethodField()
        medicacao = serializers.SerializerMethodField()
        paciente_nome = serializers.SerializerMethodField()
        medico = serializers.SerializerMethodField()
        tipo_parenteral_nome = serializers.SerializerMethodField()
        situacao_medicacao_atendimento = serializers.SerializerMethodField()
        tipo_posologia = serializers.SerializerMethodField()
        numero_tipo_posologia = serializers.SerializerMethodField()
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
                        'aplicacao',
                        'situacao',
                        'situacao_medicacao_atendimento',
                        'tipo_posologia',
                        'numero_tipo_posologia',
                        'dose_unica',
                        'medicamento_controlado',
                        'lista_chamada_solicitacao',
                )

        def get_medicamento_nome(self, obj):
                return obj.medicacao.nome_medicamento
        
        def get_admin_medicamentosa_nome(self, obj):
                return obj.get_admin_medicamentosa_display()
        
        def get_medico_nome(self, obj):
                return obj.medico.nome_profissional
        
        def get_medicacao(self, obj):
                return {'value': obj.medicacao.id, 'text': obj.medicacao.nome_medicamento, 'quantidade': obj.medicacao.quantidade} if obj.medicacao else {'value': None, 'text': None, 'quantidade': None}
        
        def get_paciente_nome(self, obj):
                return obj.atendimento.paciente.nome_paciente
        
        def get_medico(self, obj):
                return {'id': obj.medico.id, 'nome': obj.medico.nome_profissional } if obj.medico else {'id': None, 'nome': None }
        
        def get_tipo_parenteral_nome(self, obj):
                return obj.get_tipo_parenteral_display()
        
        def get_situacao_medicacao_atendimento(self, obj):
                medicacoes_atendimento = SituacaoMedicacaoAtendimento.objects.filter(medicacao_atendimento=obj.id).annotate(nome_enfermeiro=F('enfermeiro__nome_profissional')).order_by('data_hora_aplicacao').values('nome_enfermeiro', 'data_hora_aplicacao', 'cancelado')
                return medicacoes_atendimento
        
        def get_tipo_posologia(self, obj):
                if obj.tipo_posologia == MedicacaoAtendimento.HORAS:
                        return 'HORAS'
                elif obj.tipo_posologia == MedicacaoAtendimento.MINUTOS:
                        return 'MINUTOS'
                return None
        
        def get_numero_tipo_posologia(self, obj):
                return obj.tipo_posologia
                  