from uuid import UUID
from django.utils import timezone
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from rest_framework.exceptions import ValidationError
from rest_framework.generics import UpdateAPIView, ListAPIView

from ..serializers.urgencia import (
    PacienteSerializer, AtualizarChamadoUpdateSerializer, AtendimentoMedicoListSerializer, 
    ListagemHistoricoEvolucaoSerializer, EvolucaoAtendimento, ListagemHistoricoDiagnosticoSerializer,
    ListagemExamesSerializer, ListagemProcedimentosSerializer, ListagemAnamneseSerializer, 
    AtualizarAnamneseSerializer, DocumentacaoPacienteSerializer, HistoricoAnterioresSerializer,
    MedicacaoAtendimentoSerializer, justificativaProcedimentosSerializer
)

from publicmanager.saude_farmacia.models import Medicamento
from publicmanager.comum.utils import CsrfSessionAuthentication, SimpleAPIPagination
from publicmanager.saude_cadastro.models import CID, Exame, Profissional, Procedimento, TipoExame, TipoClassificacaoRisco
from publicmanager.saude_enfermagem.models import (
    ListaChamadaSolicitacaoAtendimento, SituacaoMedicacaoAtendimento, RequisicaoSolicitacaoAtendimento, ListaChamadoAdministracaoMedicamento, 
    ReaberturaSolicitacaoAtendimento
)
from publicmanager.saude_atendimento.models import (
    ListaChamada, Paciente, ClassificacaoRisco, AtendimentoMedico, DiagnosticoAtendimento, ExameAtendimento, ProcedimentoAtendimento,
    AnamnesePaciente, DocumentoPaciente, BoletimPaciente, MedicacaoAtendimento, JustificativaProcedimentoAtendimento, ListaChamadaClassificacaoRisco,
    ReaberturaAtendimentoMedico
)

class PacienteListAPIView(ListAPIView):
    serializer_class = PacienteSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if len(query) < 3:
            return Paciente.objects.none()

        items = Paciente.objects.filter(nome_paciente__icontains=query)[:5]
        serializer = PacienteSerializer(items, many=True)
        return Response(serializer.data)

class PacienteDetalheAPIView(APIView):
    def get(self, request):
        paciente_id = request.query_params.get('paciente_id', '')
        resultado = Paciente.objects.get(id=paciente_id)
        if resultado is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PacienteSerializer(resultado)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AtualizarChamadoUpdateAPIView(UpdateAPIView):
    serializer_class = AtualizarChamadoUpdateSerializer
    queryset = ListaChamada.objects.all()
    authentication_classes = (CsrfSessionAuthentication, )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.contagem = instance.contagem + 1
        instance.save()

        return Response({'contagem': instance.contagem}, status=status.HTTP_200_OK)
    
class AtualizarChamadoClassificacaoUpdateAPIView(UpdateAPIView):
    queryset = ListaChamadaClassificacaoRisco.objects.all()
    authentication_classes = (CsrfSessionAuthentication, )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.sala = self.request.user.get_unidade_login().sala
        instance.contagem = instance.contagem + 1
        instance.save()

        return Response({'contagem': instance.contagem}, status=status.HTTP_200_OK)
    
class FinalizarBoletimAtendimentoUpdateAPIView(UpdateAPIView):
    queryset = BoletimPaciente.objects.all()
    authentication_classes = (CsrfSessionAuthentication, )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        boletim_situacao = request.data.get('situacao')

        if instance.tipo == BoletimPaciente.MEDICACAO:
            lista_chamado_administracao_medicamento = ListaChamadoAdministracaoMedicamento.objects.filter(boletim__id=instance.id).first()
            if lista_chamado_administracao_medicamento:
                lista_chamado_administracao_medicamento.situacao = ListaChamadoAdministracaoMedicamento.ENCERRADO_RECEPCAO
                lista_chamado_administracao_medicamento.save()
           
        else:
            chamado_id = request.data.get('chamado_id', '')
            chamado_situacao = request.data.get('situacao_chamado', '')

            if chamado_id and chamado_situacao:
                lista_chamada =  ListaChamada.objects.filter(pk=chamado_id).first()
                lista_chamada.situacao = int(chamado_situacao)
                lista_chamada.save()

            elif chamado_situacao:
                lista = ListaChamada.objects.filter(classificacao_risco__boletim__id=instance.id).first()
                if lista: 
                    lista.situacao = int(chamado_situacao)
                    lista.save()

        instance.situacao = int(boletim_situacao)
        instance.data_saida = timezone.now()
        instance.save()

        return Response(status=status.HTTP_200_OK)
    
class AtendimentoMedicoViewSet(viewsets.ModelViewSet):
    queryset = AtendimentoMedico.objects.all()
    serializer_class = AtendimentoMedicoListSerializer
    authentication_classes = (CsrfSessionAuthentication, )
    pagination_class = SimpleAPIPagination

    # Atendimento Médico
    @action(detail=True, methods=['GET'])
    def get_atendimento_medico(self, request, pk=None):
        try:
            atendimento_medico = AtendimentoMedico.objects.get(pk=pk)
        except AtendimentoMedico.DoesNotExist:
            return Response({"error": "Atendimento Médico não encontrado"}, status=404)
        
        serializer = AtendimentoMedicoListSerializer(instance=atendimento_medico, context={'request': request})
        return Response(serializer.data)
    
    # Criar Histórico Diagnóstico
    @action(detail=True, methods=['POST', 'PUT'])
    def criar_atualizar_historico_evolucao(self, request, pk=None):
        profissional = Profissional.objects.get(user=request.user)
        regsitro_evolucao = self.request.data.get('evolucao')
        retorno = self.request.data.get('retorno')

        if request.method == 'POST':
            atendimento_medico = AtendimentoMedico.objects.get(pk=pk)

            EvolucaoAtendimento.objects.create(
                profissional=profissional,
                atendimento=atendimento_medico, 
                registro_evolucao=regsitro_evolucao,
                retorno=retorno,
            )
        elif request.method == 'PUT':
            evolucao_instance = EvolucaoAtendimento.objects.get(pk=pk)
            evolucao_instance.registro_evolucao = regsitro_evolucao
            evolucao_instance.retorno = retorno
            evolucao_instance.save()

            atendimento_medico = evolucao_instance.atendimento

        evolucao_list = EvolucaoAtendimento.objects.filter(atendimento=atendimento_medico).order_by('-created_at')
        return Response(ListagemHistoricoEvolucaoSerializer(instance=evolucao_list, many=True).data)
    
    #Criar de diagnosticos
    @action(detail=True, methods=['POST'])
    def criar_diagnostico_atendimento(self, request, pk=None):
        atendimento_medico = AtendimentoMedico.objects.get(pk=pk)
        profissional = Profissional.objects.get(user=request.user)
        arquivo = self.request.data.get('arquivo')
        descricao = self.request.data.get('descricao')
        nome_arquivo = self.request.data.get('nome_arquivo')
        
        cid_instance = get_object_or_404(CID, pk=self.request.data.get('cid'))

        DiagnosticoAtendimento.objects.create(
            cid=cid_instance, arquivo=arquivo, atendimento=atendimento_medico, 
            descricao=descricao, profissional=profissional, nome_arquivo = nome_arquivo
        )

        diagnostico_list = DiagnosticoAtendimento.objects.filter(atendimento=atendimento_medico).order_by('-created_at')
        return Response(ListagemHistoricoDiagnosticoSerializer(instance=diagnostico_list, many=True).data)
    
    # Listar Criar, Atualizar e Deletar exame atendimento
    @action(detail=True, methods=['GET', 'POST', 'PUT', 'DELETE'])
    def exame_atendimento(self, request, pk=None):
        try:
            if request.method == 'GET':
                exames_list = ExameAtendimento.objects.filter(atendimento__pk=pk).order_by('-created_at')

                return Response(ListagemExamesSerializer(instance=exames_list, many=True).data)

            if request.method == 'POST':
                atendimento_medico = AtendimentoMedico.objects.get(pk=pk)
                medico_solicitante = Profissional.objects.get(user=request.user)
                observacao = self.request.data.get('observacao')

                exame_instance = get_object_or_404(Exame, pk=self.request.data.get('exame'))

                ExameAtendimento.objects.create(
                    atendimento=atendimento_medico, exame=exame_instance, 
                    medico_solicitante=medico_solicitante, observacao=observacao
                )

                exame_list = ExameAtendimento.objects.filter(atendimento=atendimento_medico).order_by('-created_at')

                return Response(ListagemExamesSerializer(instance=exame_list, many=True).data)
                
            if request.method == 'PUT':
                arquivo_nome = self.request.data.get('arquivo_nome')
                arquivo = self.request.data.get('arquivo')
                
                instance = ExameAtendimento.objects.get(pk=pk)
                instance.arquivo_nome = arquivo_nome
                instance.arquivo = arquivo
                instance.save()

                return Response(ListagemExamesSerializer(instance=instance).data)

            if request.method == 'DELETE':
               
                try:
                    exame = ExameAtendimento.objects.get(pk=pk)
                except ProcedimentoAtendimento.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)

                arquivo_path = exame.arquivo.path if exame.arquivo else None

                if arquivo_path:
                    default_storage.delete(arquivo_path)

                exame.delete()
                return Response(status=status.HTTP_200_OK)

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # Listar Criar, Atualizar e Deletar procedimento atendimento
    @action(detail=True, methods=['GET', 'POST', 'PUT', 'DELETE'])
    def procedimento_atendimento(self, request, pk=None):
        try:
            if request.method == 'GET':
                atendiemnto_exames = ProcedimentoAtendimento.objects.filter(atendimento__pk=pk).order_by('-created_at')

                return Response(ListagemProcedimentosSerializer(instance=atendiemnto_exames, many=True).data)
            
            if request.method == 'POST':
                atendimento_medico = AtendimentoMedico.objects.get(pk=pk)
                medico_solicitante = Profissional.objects.get(user=request.user)
                quantidade = self.request.data.get('quantidade')
                classificacao = self.request.data.get('classificacao')
                tipo_solicitacao = self.request.data.get('tipo_solicitacao')
                realizado_por = self.request.data.get('realizado_por')
                
                procedimento = get_object_or_404(Procedimento, pk=self.request.data.get('procedimento'))

                ProcedimentoAtendimento.objects.create(
                    atendimento = atendimento_medico, medico_solicitante = medico_solicitante, procedimento = procedimento, 
                    quantidade = quantidade, classificacao = classificacao, tipo_solicitacao=int(tipo_solicitacao), realizado_por=int(realizado_por)
                )

                procedimentos_list = ProcedimentoAtendimento.objects.filter(atendimento=atendimento_medico).order_by('-created_at')
                return Response(ListagemProcedimentosSerializer(instance=procedimentos_list, many=True).data)
            
            if request.method == 'PUT':
                quantidade = self.request.data.get('quantidade')
                classificacao = self.request.data.get('classificacao')
                tipo_solicitacao = self.request.data.get('tipo_solicitacao')
                realizado_por = self.request.data.get('realizado_por')

                procedimento = get_object_or_404(Procedimento, pk=self.request.data.get('procedimento'))

                procedimento_atendimento = ProcedimentoAtendimento.objects.get(pk=pk)
                procedimento_atendimento.quantidade = quantidade
                procedimento_atendimento.classificacao = classificacao
                procedimento_atendimento.procedimento = procedimento
                procedimento_atendimento.tipo_solicitacao = int(tipo_solicitacao)
                procedimento_atendimento.realizado_por=int(realizado_por)
                procedimento_atendimento.save()
                
                return Response(ListagemProcedimentosSerializer(instance=procedimento_atendimento).data)
                
            if request.method == 'DELETE':
                try:
                    procedimento_atendimento = ProcedimentoAtendimento.objects.get(pk=pk)
                except ProcedimentoAtendimento.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)

                arquivo_path = procedimento_atendimento.arquivo.path if procedimento_atendimento.arquivo else None

                if arquivo_path:
                    default_storage.delete(arquivo_path)

                procedimento_atendimento.delete()

                return Response(status=status.HTTP_200_OK)

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # Listar Justificativa do procedimento do atendimento
    @action(detail=True, methods=['GET'])
    def get_justificativa_procedimento_atendimento(self, request, pk=None):
        try:
            atendimento_procedimento = JustificativaProcedimentoAtendimento.objects.get(atendimento__pk=pk)
            serialized_data = justificativaProcedimentosSerializer(instance=atendimento_procedimento, many=False).data
            return Response(serialized_data)
        except JustificativaProcedimentoAtendimento.DoesNotExist:
            return Response(None, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Listar, Atualizar histórico patologico  
    @action(detail=True, methods=['GET', 'PUT'])
    def historico_patologico(self, request, pk=None):
        try:
            if request.method == 'GET':
                atendimento_medico = AtendimentoMedico.objects.get(pk=pk)
                
                serializer = ListagemAnamneseSerializer(instance=atendimento_medico.paciente.anamnese_paciente , many=False)
                
                return Response(serializer.data)

            if request.method == 'PUT':
                anamnese = get_object_or_404(AnamnesePaciente, pk=pk)
                alergias_medicamentosas_str = request.data.get('alergias_medicamentosas', '')
                antecedentes_patologicos_pessoais_str = request.data.get('antecedentes_patologicos_pessoais', '')
                antecedentes_patologicos_familiares_str = request.data.get('antecedentes_patologicos_familiares', '')

                data_copy = request.data.copy()

                if 'tempo_situacao_de_rua' in data_copy and data_copy['tempo_situacao_de_rua'] == 'null':
                    data_copy['tempo_situacao_de_rua'] = None

                if 'frequencia_diaria_alimentacao' in data_copy and data_copy['frequencia_diaria_alimentacao'] == 'null':
                    data_copy['frequencia_diaria_alimentacao'] = None

                if 'situacao_peso' in data_copy and data_copy['situacao_peso'] == 'null':
                    data_copy['situacao_peso'] = None

                serializer = AtualizarAnamneseSerializer(anamnese, data=data_copy, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                if alergias_medicamentosas_str:
                    alergias_medicamentosas_uuids = alergias_medicamentosas_str.split(',')
                    alergias_medicamentosas = [UUID(uuid) for uuid in alergias_medicamentosas_uuids]
                    anamnese.alergias_medicamentosas.set(alergias_medicamentosas)
                else:
                    anamnese.alergias_medicamentosas.set([])

                if antecedentes_patologicos_pessoais_str:
                    antecedentes_patologicos_pessoais_uuids = antecedentes_patologicos_pessoais_str.split(',')
                    antecedentes_patologicos_pessoais = [UUID(uuid) for uuid in antecedentes_patologicos_pessoais_uuids]
                    anamnese.antecedentes_patologicos_pessoais.set(antecedentes_patologicos_pessoais)
                else:
                    anamnese.antecedentes_patologicos_pessoais.set([])

                if antecedentes_patologicos_familiares_str:
                    patologicos_familiares_uuids = antecedentes_patologicos_familiares_str.split(',')
                    patologicos_pessoais = [UUID(uuid) for uuid in patologicos_familiares_uuids]
                    anamnese.antecedentes_patologicos_familiares.set(patologicos_pessoais)
                else:
                    anamnese.antecedentes_patologicos_familiares.set([])
                anamnese.save()

                return Response(serializer.data, status=status.HTTP_200_OK)
            
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    # Listar Criar, Atualizar e Deletar documentação do Paciente
    @action(detail=True, methods=['GET', 'POST', 'PUT', 'DELETE'])
    def documentacao_paciente(self, request, pk=None):
        try:
            if request.method == 'GET':
                atendimento_medico = AtendimentoMedico.objects.get(pk=pk)
               
                serializer = DocumentacaoPacienteSerializer(instance=DocumentoPaciente.objects.filter(paciente=atendimento_medico.paciente), many=True)
                
                return Response(serializer.data)
            
            if request.method == 'POST':
                atendimento_medico = AtendimentoMedico.objects.get(pk=pk)
                profissional = Profissional.objects.get(user=request.user)
                nome = self.request.data.get('nome')
                arquivo = self.request.data.get('arquivo')
                descricao = self.request.data.get('descricao')

                DocumentoPaciente.objects.create(
                    nome=nome,  
                    arquivo=arquivo,
                    paciente=atendimento_medico.paciente,
                    descricao=descricao,
                    profissional=profissional,
                )

                documentacoes = DocumentoPaciente.objects.filter(paciente=atendimento_medico.paciente).order_by('-created_at')

                return Response(DocumentacaoPacienteSerializer(instance=documentacoes, many=True).data)

            if request.method == 'PUT':
                documento = get_object_or_404(DocumentoPaciente, pk=pk)
                if self.request.data.get('arquivo'):
                    documento.nome = self.request.data.get('nome')
                    documento.arquivo = self.request.data.get('arquivo')
                documento.descricao = self.request.data.get('descricao')
                documento.save()

                return Response(DocumentacaoPacienteSerializer(instance=documento).data)

            if request.method == 'DELETE':
                documento = DocumentoPaciente.objects.get(pk=pk)
                documento.delete()

                return Response(status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    # Listar históricos anteriores  
    @action(detail=True, methods=['GET'])
    def get_historico_ateriores(self, request, pk=None):
        paciente = Paciente.objects.get(pk=pk)
     
        boletins = BoletimPaciente.objects.exclude(
            situacao__in=[BoletimPaciente.EM_ABERTO, BoletimPaciente.EM_ANDAMENTO]
        ).filter(paciente=paciente).order_by('-created_at')

        result_page = self.paginate_queryset(boletins)
        
        serializer = HistoricoAnterioresSerializer(instance=result_page, many=True)
        
        return self.get_paginated_response(serializer.data)
    
    # Listar Criar e Deletar medicação do atendimento
    @action(detail=True, methods=['GET', 'POST', 'PUT', 'DELETE'])
    def medicacao_atendimento(self, request, pk=None):
        try:
            if request.method == 'GET':
                atendimento_medico = AtendimentoMedico.objects.get(pk=pk)
                medicacoes_atendimentos = MedicacaoAtendimento.objects.filter(atendimento=atendimento_medico).order_by('situacao')

                serializer = MedicacaoAtendimentoSerializer(instance=medicacoes_atendimentos, many=True)
                return Response(serializer.data)
            
            if request.method == 'POST':
                atendimento_medico = AtendimentoMedico.objects.get(pk=pk)
                medico = Profissional.objects.get(user=request.user)
                via_admin = self.request.data.get('via')
                parenteral = self.request.data.get('parental')
                dosagem = self.request.data.get('dosagem')
                posologia = self.request.data.get('posologia')
                tipo_posologia = self.request.data.get('tipo_posologia')
                uso_continuo = self.request.data.get('uso_continuo').capitalize() if self.request.data.get('uso_continuo') else False
                duracao_tratamento = self.request.data.get('duracao_tratamento')
                observacao = self.request.data.get('observacao')
                aplicacao = self.request.data.get('aplicacao')
                estoque_zero = self.request.data.get('estoque_zero').capitalize() if self.request.data.get('estoque_zero') else False
                dose_unica = self.request.data.get('dose_unica').capitalize() if self.request.data.get('dose_unica') else False
                medicamento_controlado = self.request.data.get('medicamento_controlado').capitalize() if self.request.data.get('medicamento_controlado') else False

                farmacia_medicacao = Medicamento.objects.get(pk=self.request.data.get('medicacao'))

                tipo_parenteral = None
                if via_admin == '1':
                    tipo_parenteral = int(parenteral)

                MedicacaoAtendimento.objects.create(
                    atendimento=atendimento_medico,  
                    medico=medico,
                    admin_medicamentosa=int(via_admin),
                    tipo_parenteral=tipo_parenteral,
                    medicacao=farmacia_medicacao,
                    dosagem=dosagem,
                    posologia=posologia,
                    uso_continuo=uso_continuo,
                    duracao_tratamento=duracao_tratamento,
                    observacao=observacao,
                    aplicacao=aplicacao,
                    dose_unica=dose_unica,
                    medicamento_controlado=medicamento_controlado,
                    tipo_posologia=tipo_posologia,
                    estoque_zero=estoque_zero
                )
                medicacao_atendimento = MedicacaoAtendimento.objects.filter(atendimento=atendimento_medico).order_by('-created_at')
                return Response(MedicacaoAtendimentoSerializer(instance=medicacao_atendimento, many=True).data)

            if request.method == 'PUT':
                medicacao_atendimento = MedicacaoAtendimento.objects.get(pk=pk)
                via_admin = self.request.data.get('via')
                parenteral = self.request.data.get('parental')
                dosagem = self.request.data.get('dosagem')
                posologia = self.request.data.get('posologia')
                tipo_posologia = self.request.data.get('tipo_posologia')
                uso_continuo = self.request.data.get('uso_continuo').capitalize() if self.request.data.get('uso_continuo') else False
                duracao_tratamento = self.request.data.get('duracao_tratamento')
                observacao = self.request.data.get('observacao')
                aplicacao = self.request.data.get('aplicacao')
                estoque_zero = self.request.data.get('estoque_zero').capitalize() if self.request.data.get('estoque_zero') else False
                dose_unica = self.request.data.get('dose_unica').capitalize() if self.request.data.get('dose_unica') else False
                medicamento_controlado = self.request.data.get('medicamento_controlado').capitalize() if self.request.data.get('medicamento_controlado') else False

                farmacia_medicacao = Medicamento.objects.get(pk=self.request.data.get('medicacao'))

                tipo_parenteral = None
                if via_admin == '1':
                    tipo_parenteral = int(parenteral)

                medicacao_atendimento.admin_medicamentosa = int(via_admin)
                medicacao_atendimento.tipo_parenteral = tipo_parenteral
                medicacao_atendimento.medicacao = farmacia_medicacao
                medicacao_atendimento.dosagem = dosagem
                medicacao_atendimento.posologia = posologia
                medicacao_atendimento.uso_continuo = uso_continuo
                medicacao_atendimento.duracao_tratamento = duracao_tratamento
                medicacao_atendimento.observacao = observacao
                medicacao_atendimento.aplicacao = aplicacao
                medicacao_atendimento.dose_unica = dose_unica
                medicacao_atendimento.medicamento_controlado = medicamento_controlado
                medicacao_atendimento.tipo_posologia = int(tipo_posologia)
                medicacao_atendimento.estoque_zero = estoque_zero
                medicacao_atendimento.save()

                medicacao_atendimento = MedicacaoAtendimento.objects.filter(atendimento=medicacao_atendimento.atendimento).order_by('-created_at')
                return Response(MedicacaoAtendimentoSerializer(instance=medicacao_atendimento, many=True).data)
            
            if request.method == 'DELETE':
                medicacao = MedicacaoAtendimento.objects.get(pk=pk)

                SituacaoMedicacaoAtendimento.objects.filter(medicacao_atendimento=medicacao).delete()
                
                medicacao.delete()

                return Response(status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    # Listar Criar e Deletar medicação do atendimento
    @action(detail=True, methods=['POST'])
    def reclassificacao(self, request, pk=None):
        atendimento_medico = AtendimentoMedico.objects.get(pk=pk)

        queixa_principal = self.request.data.get('queixa_principal')
        peso = self.request.data.get('peso')
        altura = self.request.data.get('altura')
        escala_dor = self.request.data.get('escala_dor') if self.request.data.get('escala_dor') else None
        estado_geral = self.request.data.get('estado_geral') if self.request.data.get('estado_geral') else None
        tipo_classificacao_risco_id = self.request.data.get('tipo_classificacao_risco_id')
        observacao = self.request.data.get('observacao')
        presao_arterial = self.request.data.get('presao_arterial')
        frequencia_cardiaca = self.request.data.get('frequencia_cardiaca')
        frequencia_respiratoria = self.request.data.get('frequencia_respiratoria')
        temperatura = self.request.data.get('temperatura')
        spo2 = self.request.data.get('spo2')
        hgt = self.request.data.get('hgt')
        
        profissional = Profissional.objects.get(user=request.user)
        tipo_classificacao_risco = TipoClassificacaoRisco.objects.get(id=tipo_classificacao_risco_id)

        classificacao_risco = ClassificacaoRisco.objects.filter(atendimentomedico=pk).order_by('created_at')
        
        if classificacao_risco.filter(profissional=profissional, setor=ClassificacaoRisco.ATENDIMENTO_MEDICO).exists():
            classificacao_risco = classificacao_risco.filter(profissional=profissional, setor=ClassificacaoRisco.ATENDIMENTO_MEDICO).first()

            classificacao_risco.paciente=classificacao_risco.paciente
            classificacao_risco.profissional=profissional
            classificacao_risco.boletim=classificacao_risco.boletim
            classificacao_risco.data_hora_avaliacao=timezone.now()
            classificacao_risco.queixa_principal=queixa_principal
            classificacao_risco.peso=None if not peso or peso == 'null' else float(peso)
            classificacao_risco.altura=None if not altura or altura == 'null' else float(altura)
            classificacao_risco.escala_dor=escala_dor
            classificacao_risco.estado_geral=estado_geral
            classificacao_risco.observacao=None if not observacao or observacao == 'null' else observacao
            classificacao_risco.tipo_atendimento=classificacao_risco.tipo_atendimento
            classificacao_risco.presao_arterial=None if not presao_arterial or presao_arterial == 'null' else presao_arterial
            classificacao_risco.tipo_classificacao_risco=tipo_classificacao_risco
            classificacao_risco.frequencia_cardiaca=None if not frequencia_cardiaca or frequencia_cardiaca == 'null' else frequencia_cardiaca
            classificacao_risco.frequencia_respiratoria=None if not frequencia_respiratoria or frequencia_respiratoria == 'null' else frequencia_respiratoria
            classificacao_risco.temperatura=None if not temperatura or temperatura == 'null' else temperatura
            classificacao_risco.spo2=None if not spo2 or spo2 == 'null' else spo2
            classificacao_risco.hgt=None if not hgt or hgt == 'null' else hgt
            classificacao_risco.save()

        else:

            reclassificacao_risco = classificacao_risco.order_by('-created_at').first()
            create_classificacao = ClassificacaoRisco.objects.create(
                paciente=reclassificacao_risco.paciente,
                profissional=profissional,
                boletim=reclassificacao_risco.boletim,
                data_hora_avaliacao=timezone.now(),
                queixa_principal=queixa_principal,
                peso=None if not peso or peso == 'null' else float(peso),
                altura=None if not altura or altura == 'null' else float(altura),
                escala_dor=escala_dor,
                estado_geral=estado_geral,
                observacao=None if not observacao or observacao == 'null' else observacao,
                reclassificacao=True,
                setor=ClassificacaoRisco.ATENDIMENTO_MEDICO,
                tipo_atendimento=reclassificacao_risco.tipo_atendimento,
                numero_atendimento=reclassificacao_risco.numero_atendimento,
                presao_arterial=None if not presao_arterial or presao_arterial == 'null' else presao_arterial,
                tipo_classificacao_risco=tipo_classificacao_risco,
                frequencia_cardiaca=None if not frequencia_cardiaca or frequencia_cardiaca == 'null' else frequencia_cardiaca,
                frequencia_respiratoria=None if not frequencia_respiratoria or frequencia_respiratoria == 'null' else frequencia_respiratoria,
                temperatura=None if not temperatura or temperatura == 'null' else temperatura,
                spo2=None if not spo2 or spo2 == 'null' else spo2,
                hgt=None if not hgt or hgt == 'null' else hgt,
            )

            reclassificacao_risco.status = ClassificacaoRisco.DESABILITADO
            reclassificacao_risco.save()

            atendimento_medico.classificacao_risco.add(create_classificacao)
            atendimento_medico.save()
            
            atendimento_medico.lista_chamada.classificacao_risco = create_classificacao
            atendimento_medico.lista_chamada.save()

        return Response(status=status.HTTP_200_OK)
        
    #Criar de ordenação
    @action(detail=True, methods=['POST'])
    def criar_ordenacao_atendimento(self, request, pk=None):
        atendimento_medico = AtendimentoMedico.objects.get(pk=pk)
        ordenacoes = request.data.get('ordenacoes', [])

        if ordenacoes:

            requisicao = RequisicaoSolicitacaoAtendimento.objects.create(
                atendimento=atendimento_medico,
                medico_solicitante=self.request.user.profissional_set.first()
            )

            for index, ordenacao in enumerate(ordenacoes):
                # Define os valores padrão a serem usados ​​em todos os casos
                defaults = {
                    'atendimento': atendimento_medico,
                    'unidade_saude': atendimento_medico.unidade_saude,
                    'tipo': int(ordenacao['tipo']),
                    'sequencial': int(ordenacao['number']),
                }

                # Adiciona a situacao se é o primeiro item
                if index == 0:
                    defaults['situacao'] = 1

                # Cria ou obtém o objeto ListaChamadaSolicitacaoAtendimento
                chamada_solicitacao = ListaChamadaSolicitacaoAtendimento.objects.create(**defaults)

                if defaults['tipo'] == 0:
                    exames_laboratoriais = ExameAtendimento.objects.filter(atendimento=atendimento_medico, exame__tipo_exame__tipo=TipoExame.LABORATORIO, situacao=ExameAtendimento.SOLICITADO)
                    if exames_laboratoriais:
                        for exame in exames_laboratoriais:
                            exame.lista_chamada_solicitacao = chamada_solicitacao
                            exame.save()

                elif defaults['tipo'] == 1:
                    exames_imagens = ExameAtendimento.objects.filter(atendimento=atendimento_medico, exame__tipo_exame__tipo=TipoExame.IMAGEM, situacao=ExameAtendimento.SOLICITADO)
                    if exames_imagens:
                        for exame in exames_imagens:
                            exame.lista_chamada_solicitacao = chamada_solicitacao
                            exame.save()

                elif defaults['tipo'] == 2:
                    procedimentos_atendimento = ProcedimentoAtendimento.objects.filter(atendimento=atendimento_medico, situacao=ProcedimentoAtendimento.SOLICITADO, tipo_solicitacao=ProcedimentoAtendimento.INTERNO, realizado_por=ProcedimentoAtendimento.ENFERMAGEM)
                    
                    if procedimentos_atendimento:
                        for procedimento in procedimentos_atendimento:
                            procedimento.lista_chamada_solicitacao = chamada_solicitacao
                            procedimento.save()
                
                elif defaults['tipo'] == 3:
                    medicacoes = MedicacaoAtendimento.objects.filter(atendimento=atendimento_medico, situacao=MedicacaoAtendimento.SOLICITADO)
                    
                    if medicacoes:
                        for medicacao in medicacoes:
                            medicacao.lista_chamada_solicitacao = chamada_solicitacao
                            medicacao.save()


                requisicao.listas_chamadas_solicitacoes.add(chamada_solicitacao)

        atendimento_medico.lista_chamada.situacao = ListaChamada.EM_PROCEDIMENTO
        atendimento_medico.lista_chamada.save()
        
        return Response(data={'situacao': atendimento_medico.lista_chamada.get_situacao_display()}, status=status.HTTP_200_OK)

    # Reabertura da Solicitação
    @action(detail=True, methods=['PUT'])
    def reabertura_solicitacao(self, request, pk=None):
        try:
            if request.method != 'PUT':
                return Response({"detail": "Método não permitido."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

            tipo = request.data.get('tipo')
            justificativa = request.data.get('justificativa')
            user = request.user

            tipos_mapeados = {
                'exame': ExameAtendimento,
                'medicacao': MedicacaoAtendimento,
                'procedimento': ProcedimentoAtendimento,
            }

            if tipo not in tipos_mapeados:
                return Response({"detail": "Tipo inválido."}, status=status.HTTP_400_BAD_REQUEST)

            atendimento_model = tipos_mapeados[tipo]
            atendimento_instance = get_object_or_404(atendimento_model, id=pk)

            atendimento_instance.situacao = atendimento_model.REABERTURA
            atendimento_instance.save()

            lista_chamada_solicitacao = get_object_or_404(
                ListaChamadaSolicitacaoAtendimento,
                id=atendimento_instance.lista_chamada_solicitacao.id
            )
            lista_chamada_solicitacao.situacao = ListaChamadaSolicitacaoAtendimento.REABERTURA
            lista_chamada_solicitacao.save()

            ReaberturaSolicitacaoAtendimento.objects.create(
                lista_chamada_solicitacao=lista_chamada_solicitacao,
                medico_solicitante=get_object_or_404(Profissional, user=user),
                justificativa=justificativa,
            )

            return Response({"detail": "Reabertura realizada com sucesso."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    # Reabertura da Solicitação
    @action(detail=True, methods=['PUT'])
    def reabertura_atendimento_medico(self, request, pk=None):
        try:
            if request.method != 'PUT':
                return Response({"detail": "Método não permitido."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
            if not pk:
                return Response({"detail": "PK não permitido"}, status=status.HTTP_400_BAD_REQUEST)

            justificativa = request.data.get('justificativa')
            user = request.user

            if not justificativa:
                return Response({"detail": "Justificativa não existe"}, status=status.HTTP_400_BAD_REQUEST)

            profissional = Profissional.objects.get(user=user)

            atendimento_medico = AtendimentoMedico.objects.filter(id=pk).first()
            if not atendimento_medico:
                return Response({"detail": "Atendimento Médico não existe"}, status=status.HTTP_400_BAD_REQUEST)
            
            atendimento_medico.lista_chamada.situacao = ListaChamada.ATENDIMENTO_REABERTO
            atendimento_medico.lista_chamada.save()

            ReaberturaAtendimentoMedico.objects.create(
                atendimento=atendimento_medico,
                profissional=profissional,
                justificativa=justificativa
            )

            return Response({
                "detail": "Reabertura realizada com sucesso.",
                "status_lista_chamada_numero": atendimento_medico.lista_chamada.situacao,
                "status_lista_chamada": atendimento_medico.lista_chamada.get_situacao_display()
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    # Suspender Confirmar Procedimento Médico
    @action(detail=True, methods=['PUT'])
    def suspender_confirmar_procedimento(self, request, pk=None):
        try:
            if not pk:
                return Response({"detail": "PK não permitido"}, status=status.HTTP_400_BAD_REQUEST)
            
            tipo = int(self.request.data.get('tipo'))
            justificativa = self.request.data.get('justificativa')

            profissional = Profissional.objects.get(user=request.user)
            
            atendimento_procedimento = ProcedimentoAtendimento.objects.get(id=pk)
            if not atendimento_procedimento:
                return Response({"detail": "Procedimento não existe"}, status=status.HTTP_400_BAD_REQUEST)
            
            atendimento_procedimento.situacao = tipo
            atendimento_procedimento.profissional_responsavel = profissional

            if tipo == 1:
                atendimento_procedimento.justificativa = justificativa

            atendimento_procedimento.save()

            return Response(ListagemProcedimentosSerializer(instance=atendimento_procedimento, many=False).data)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class AtendimentoRetornoBoletimMedicacaoUpdateAPIView(UpdateAPIView):
    queryset = BoletimPaciente.objects.all()
    authentication_classes = (CsrfSessionAuthentication, )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        boletim_situacao = request.data.get('situacao')

        if instance.tipo == BoletimPaciente.MEDICACAO:
            lista_chamado_administracao_medicamento = ListaChamadoAdministracaoMedicamento.objects.get(boletim__id=instance.id)
            lista_chamado_administracao_medicamento.situacao = ListaChamadoAdministracaoMedicamento.EM_ESPERA
            lista_chamado_administracao_medicamento.contagem = 0
            lista_chamado_administracao_medicamento.save(skip_hooks=True)
           
        instance.situacao = int(boletim_situacao)
        instance.save()

        return Response(status=status.HTTP_200_OK)