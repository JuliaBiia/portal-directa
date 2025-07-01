import json
from datetime import timedelta
from django.utils import timezone
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from rest_framework.generics import UpdateAPIView, CreateAPIView

from .serializers import (
    ChamadoSolicitacaoUpdateSerializer, AdministacaoMedicacaoSerializer, AtualizarAplicacaoSerializer, ExameAtendimentoSerializer, SolicitacoesTimeLineSerializer,
    ProcedimentosAtendimentoSerializer, ReceitaMedicamentoSerializer, SituacaoAdministracaoMedicamentoSerializer, ListaChamadoAdministracaoMedicamentoSerializer,
    SolicitacaoAdministracaoProcedimentoSerializer, SituacaoAdministracaoProcedimentoSerializer
)

from publicmanager.saude.models import UnidadeSaude
from publicmanager.saude_farmacia.models import Medicamento
from publicmanager.comum.utils import SimpleAPIPagination, CsrfSessionAuthentication
from publicmanager.saude_cadastro.models import Profissional, TipoExame, Procedimento
from publicmanager.saude_enfermagem.models import (
    ListaChamadaSolicitacaoAtendimento, SituacaoMedicacaoAtendimento, RequisicaoSolicitacaoAtendimento, ReceitaMedicamento, ListaChamadoAdministracaoMedicamento,
    AdministracaoMedicamento, SituacaoAdministracaoMedicamento, ListaChamadoAdministracaoProcedimento, ReceitaAdministracaoProcedimento, AdministracaoProcedimento, SituacaoAdministracaoProcedimento
)
from publicmanager.saude_atendimento.models import (
    AtendimentoMedico, MedicacaoAtendimento, ExameAtendimento, EvolucaoAtendimento, ListaChamada, BoletimPaciente, ProcedimentoAtendimento,
    Paciente, ArquivoExameAtendimento, ArquivoProcedimentoAtendimento
)
    
class ChamadoEnfermagemUpdateAPIView(UpdateAPIView):
    serializer_class = ChamadoSolicitacaoUpdateSerializer
    queryset = ListaChamadaSolicitacaoAtendimento.objects.all()
    authentication_classes = (CsrfSessionAuthentication, )

    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        tipo = self.request.GET.get('tipo')
        print(f"PROCEDIMENTOS ELETIVO A: {pk}")

        if tipo == 'admin_medicamento':
            lista_chamado = ListaChamadoAdministracaoMedicamento.objects.get(id=pk)
            lista_chamado.contagem = lista_chamado.contagem + 1
            lista_chamado.save()

            return Response({'contagem': lista_chamado.contagem}, status=status.HTTP_200_OK)
        elif tipo == 'admin_procedimento':
            lista_chamado = ListaChamadoAdministracaoProcedimento.objects.get(id=pk)
            lista_chamado.contagem = lista_chamado.contagem + 1
            lista_chamado.save()

            return Response({'contagem': lista_chamado.contagem}, status=status.HTTP_200_OK)
        else:
            instance = self.get_object()
            instance.contagem = instance.contagem + 1
            instance.save()

            return Response({'contagem': instance.contagem}, status=status.HTTP_200_OK)

class SolicitacoesAtendimentoViewSet(viewsets.ModelViewSet):
    queryset = ListaChamadaSolicitacaoAtendimento.objects.all()
    authentication_classes = (CsrfSessionAuthentication, )
    pagination_class = SimpleAPIPagination

    # Listar, Atualizar e Deletar Exames Laboratoriais
    @action(detail=True, methods=['GET', 'PUT', 'DELETE'])
    def exames(self, request, pk=None):
        
        if request.method == 'GET':
            tipo_exame = self.request.GET.get('tipo_exame')
            lista_chamada_pk = self.request.GET.get('lista_chamada_pk')
            lista_chamada_solicitacao = ListaChamadaSolicitacaoAtendimento.objects.get(id=lista_chamada_pk)

            tipo = None
            if tipo_exame == 'laboratorial':
                tipo = TipoExame.LABORATORIO
            elif tipo_exame == 'imagem':
                tipo = TipoExame.IMAGEM
            
            exames_list = ExameAtendimento.objects.filter(
                atendimento=lista_chamada_solicitacao.atendimento.pk, 
                exame__tipo_exame__tipo=tipo,
                lista_chamada_solicitacao=lista_chamada_solicitacao 
            ).order_by('created_at')

            return Response(ExameAtendimentoSerializer(instance=exames_list, many=True).data)
    
        if request.method == 'PUT':
            com_anexo = True if self.request.data.get('com_anexo').lower() == 'true' else False
            justificativa = self.request.data.get('justificativa')
            arquivo_nome = self.request.data.get('arquivo_nome')
            arquivos = self.request.FILES.getlist('arquivos')

            if not arquivos and not justificativa:
                return Response({'error': 'Nenhum arquivo foi enviado'}, status=status.HTTP_400_BAD_REQUEST)
            
            instance = ExameAtendimento.objects.get(pk=pk)
            instance.profissional_responsavel = self.request.user.profissional_set.first()

            if com_anexo:
                
                primeiro_arquivo = arquivos.pop(0)
                instance.situacao = ExameAtendimento.ANEXADO
                instance.arquivo_nome = primeiro_arquivo.name
                instance.arquivo = primeiro_arquivo

                for arquivo in arquivos:
                    ArquivoExameAtendimento.objects.create(
                        exame_atendimento=instance,
                        arquivo=arquivo,
                        nome=arquivo.name
                    )
            else:
                instance.situacao = ExameAtendimento.SEM_ANEXO
                instance.justificativa = justificativa
            
            instance.save()

            return Response(ExameAtendimentoSerializer(instance=instance).data)

        if request.method == 'DELETE':
            try:
                exame = ExameAtendimento.objects.get(pk=pk)
            except ExameAtendimento.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            arquivo_path = exame.arquivo.path if exame.arquivo else None
            if arquivo_path:
                default_storage.delete(arquivo_path)

            arquivos_associados = ArquivoExameAtendimento.objects.filter(exame_atendimento=exame)
            for arquivo_associado in arquivos_associados:
                arquivo_associado_path = arquivo_associado.arquivo.path if arquivo_associado.arquivo else None
                if arquivo_associado_path:
                    default_storage.delete(arquivo_associado_path)
                arquivo_associado.delete()

            exame.situacao = ExameAtendimento.SOLICITADO
            exame.arquivo = ''
            exame.arquivo_nome = ''
            exame.save()

            return Response({'situacao': exame.situacao}, status=status.HTTP_200_OK)

    # Listagem TimeLine
    @action(detail=True, methods=['GET'])
    def get_solicitacoes_timeline(self, request, pk=None):
        requisicao = RequisicaoSolicitacaoAtendimento.objects.get(listas_chamadas_solicitacoes=pk)

        return Response(SolicitacoesTimeLineSerializer(instance=requisicao, many=False).data)

    # Listar Aplicação de Medicamentos
    @action(detail=True, methods=['GET'])
    def get_aplicacao_medicacao(self, request, pk=None):
        lista_chamada_solicitacao = ListaChamadaSolicitacaoAtendimento.objects.get(id=pk)

        medicacoes_list = MedicacaoAtendimento.objects.filter(lista_chamada_solicitacao=lista_chamada_solicitacao, aplicacao=MedicacaoAtendimento.IMEDIATA).order_by('situacao')
        
        return Response(AdministacaoMedicacaoSerializer(instance=medicacoes_list, many=True).data)
    
    @action(detail=True, methods=['PUT'])
    def atualizar_situacao_aplicacao_medicacao(self, request, pk=None):
        medicacao_atendimento = get_object_or_404(MedicacaoAtendimento, pk=pk)
        tipo = self.request.data.get('tipo')
        enfermeiro_pk = self.request.data.get('enfermeiro_pk')
        observacao = self.request.data.get('observacao')
        
        enfermeiro = get_object_or_404(Profissional, pk=enfermeiro_pk)
        data_hora_atual = timezone.localtime(timezone.now())

        situacao_atendimento = SituacaoMedicacaoAtendimento.objects.create(
            medicacao_atendimento=medicacao_atendimento,
            enfermeiro=enfermeiro,
            data_hora_aplicacao=data_hora_atual,
        )

        medicacao = Medicamento.objects.get(id=medicacao_atendimento.medicacao.id)

        if tipo == 'confirmar':
            medicacao.quantidade = int(medicacao.quantidade) -1
            medicacao.save()
            
            if medicacao_atendimento.dose_unica:
                medicacao_atendimento.situacao=MedicacaoAtendimento.CONCLUIDO
                medicacao_atendimento.save()
            else:
                posologia = medicacao_atendimento.posologia.split('/')
                duracao_tratamento = int(medicacao_atendimento.duracao_tratamento) - 1

                data_futura = data_hora_atual + timedelta(days=duracao_tratamento)
                fim_do_dia = data_futura.replace(hour=23, minute=59, second=59)
                diferenca = fim_do_dia - data_hora_atual

                horas_restantes = diferenca.days * 24 + diferenca.seconds // 3600

                if medicacao_atendimento.tipo_posologia == MedicacaoAtendimento.HORAS:
                    quantidade_horas_minutos = int(horas_restantes) - int(posologia[0])
                
                elif medicacao_atendimento.tipo_posologia == MedicacaoAtendimento.MINUTOS:
                    minutos_restantes = diferenca.days * 24 * 60 + diferenca.seconds // 60
                    quantidade_tempo = minutos_restantes - int(posologia[0])

                    quantidade_horas_minutos = quantidade_tempo / 60

                if quantidade_horas_minutos <= 0:
                    medicacao_atendimento.situacao=MedicacaoAtendimento.CONCLUIDO
                    medicacao_atendimento.save()
            
        if tipo == 'suspender':

            situacao_atendimento.cancelado = True
            situacao_atendimento.observacao = observacao
            situacao_atendimento.save()

            situacao_medicacao = SituacaoMedicacaoAtendimento.objects.filter(medicacao_atendimento=medicacao_atendimento, cancelado=False).order_by('created_at').first()
            
            if situacao_medicacao:
                medicacao_atendimento.situacao=MedicacaoAtendimento.PARCIALMENTE_APLICADO
            else:
                medicacao_atendimento.situacao=MedicacaoAtendimento.SUSPENSO
            medicacao_atendimento.save()

        return Response(AtualizarAplicacaoSerializer(instance=medicacao_atendimento).data)
    
    # Procedimento Atendimento Médico - Solicitações
    @action(detail=True, methods=['GET', 'PUT'])
    def procedimentos(self, request, pk=None):

        if request.method == 'GET':
            lista_chamada_solicitacao = ListaChamadaSolicitacaoAtendimento.objects.get(id=pk)

            procedimentos_list = ProcedimentoAtendimento.objects.filter(lista_chamada_solicitacao=lista_chamada_solicitacao, tipo_solicitacao=ProcedimentoAtendimento.INTERNO).order_by('situacao')
            
            return Response(ProcedimentosAtendimentoSerializer(instance=procedimentos_list, many=True).data)
    
        if request.method == 'PUT':
            situacao = self.request.data.get('situacao')
            justificativa = self.request.data.get('justificativa')

            instance = ProcedimentoAtendimento.objects.get(pk=pk)
            instance.profissional_responsavel = self.request.user.profissional_set.first()

            if situacao == 'suspender':
                instance.situacao = ProcedimentoAtendimento.SUSPENSO
            elif situacao == 'confirmar':
                instance.situacao = ProcedimentoAtendimento.CONCLUIDO

            instance.justificativa = justificativa
            instance.save()

            return Response(ProcedimentosAtendimentoSerializer(instance=instance).data)
    
    # Procedimento Atendimento Médico - Solicitações Photo/Arquivo
    @action(detail=True, methods=['GET', 'PUT'])
    def procedimentos_photo(self, request, pk=None):

        if request.method == 'GET':
            lista_chamada_pk = self.request.GET.get('lista_chamada_pk')
            print(f"lista_chamada_pk aaaaaaaaaaaaaaaaaa: {lista_chamada_pk}")
            lista_chamada_solicitacao = ListaChamadaSolicitacaoAtendimento.objects.get(id=lista_chamada_pk)
            print(f"lista_chamada_solicitacao bbbbbbbbbbbbb: {lista_chamada_solicitacao}")

            procedimentos_list = ProcedimentoAtendimento.objects.filter(lista_chamada_solicitacao=lista_chamada_solicitacao, tipo_solicitacao=ProcedimentoAtendimento.INTERNO).order_by('situacao')
            
            return Response(ProcedimentosAtendimentoSerializer(instance=procedimentos_list, many=True).data)

        if request.method == 'PUT':
            com_anexo = True if self.request.data.get('com_anexo').lower() == 'true' else False
            situacao = self.request.data.get('situacao')
            justificativa = self.request.data.get('justificativa')
            arquivo_nome = self.request.data.get('arquivo_nome')
            arquivo = self.request.FILES.getlist('arquivo')

            if not arquivo and not justificativa:
                return Response({'error': 'Nenhum arquivo foi enviado'}, status=status.HTTP_400_BAD_REQUEST)

            instance = ProcedimentoAtendimento.objects.get(pk=pk)
            instance.profissional_responsavel = self.request.user.profissional_set.first()

            if situacao == 'CONFIRMAR':
                instance.situacao = ProcedimentoAtendimento.CONCLUIDO

            if com_anexo:
                primeiro_arquivo = arquivo.pop(0)
                instance.justificativa = justificativa
                instance.arquivo_nome = primeiro_arquivo.name
                instance.arquivo = primeiro_arquivo

                for dados in arquivo:
                    ArquivoProcedimentoAtendimento.objects.create(
                        procedimento_atendimento=instance,
                        arquivo=dados,
                        nome=dados.name
                    )

            instance.save()

            return Response(ProcedimentosAtendimentoSerializer(instance=instance).data)

    # Finalizar Processo
    @action(detail=True, methods=['PUT'])
    def finalizar_solicitacao(self, request, pk=None):
        atendimento = get_object_or_404(AtendimentoMedico, pk=pk)
        solicitacao_pk = request.data.get('solicitacao_pk')

        if not solicitacao_pk:
            return Response({'error': 'solicitacao_pk é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
        
        chamada_solicitacao = get_object_or_404(ListaChamadaSolicitacaoAtendimento, pk=solicitacao_pk)
        chamada_solicitacao.situacao = 6
        chamada_solicitacao.save()

        requisicao = get_object_or_404(RequisicaoSolicitacaoAtendimento, atendimento=atendimento, listas_chamadas_solicitacoes=chamada_solicitacao)

        lista = requisicao.listas_chamadas_solicitacoes.filter(situacao=ListaChamadaSolicitacaoAtendimento.SOLICITADO).order_by('sequencial').first()

        info = None
        if lista:
            lista.situacao = 1
            lista.save()
        else:
            info = self.processar_evolucao_e_situacao(atendimento)

        return Response({'info': info}, status=status.HTTP_200_OK)

    def processar_evolucao_e_situacao(self, atendimento):
        evolucao_list = EvolucaoAtendimento.objects.filter(atendimento=atendimento).order_by('-created_at').first()
        if atendimento.lista_chamada.situacao in [ListaChamada.EM_PROCEDIMENTO, ListaChamada.ATENDIMENTO_REABERTO]:
            if evolucao_list.retorno:
                return self.atualizar_situacao_atendimento(atendimento, ListaChamada.LISTA_RETORNO, 'retorno')
            else:
                return self.atualizar_situacao_atendimento(atendimento, ListaChamada.ENCERRADO_SISTEMA, 'encerrado')
        elif atendimento.lista_chamada.situacao in [ListaChamada.ENCERRADO_ATENDIMENTO, ListaChamada.ENCERRADO_ALTA, ListaChamada.ENCERRADO_RECEPCAO]:
            return self.atualizar_situacao_atendimento(atendimento, None, 'encerrado')

        return None

    def atualizar_situacao_atendimento(self, atendimento, nova_situacao, info):
        data_atual = timezone.now()
        if nova_situacao:
            atendimento.lista_chamada.situacao = nova_situacao
            atendimento.lista_chamada.contagem = 0
            atendimento.lista_chamada.save(skip_hooks=True)

        if info == 'encerrado':
            atendimento.lista_chamada.classificacao_risco.boletim.data_saida = data_atual
            
            if nova_situacao:
                atendimento.lista_chamada.classificacao_risco.boletim.situacao = BoletimPaciente.ENCERRADO_SISTEMA

            atendimento.lista_chamada.classificacao_risco.boletim.save()

        RequisicaoSolicitacaoAtendimento.objects.filter(atendimento=atendimento).update(finalizado=True)

        return info

class ReceitaMedicamentoCreateAPIView(CreateAPIView):
    queryset = ReceitaMedicamento.objects.all()

    def create(self, request, *args, **kwargs):
        solicitacao_id = request.data.get("solicitacao_id")
        paciente_id = request.data.get("paciente_id")
        enfermeiro_id = request.data.get("enfermeiro_id")
        unidade_saude_id = request.data.get("unidade_saude_id")
        listagem_medicamentos = request.data.get("listagem_medicamentos")
        arquivo = request.FILES.get('file')

        paciente = Paciente.objects.get(id=paciente_id)
        enfermeiro = Profissional.objects.get(id=enfermeiro_id)
        unidade_saude = UnidadeSaude.objects.get(id=unidade_saude_id)
        solicitacao = ListaChamadoAdministracaoMedicamento.objects.get(id=solicitacao_id)
       
        receita_medicamento, created = ReceitaMedicamento.objects.get_or_create(
            paciente=paciente,
            enfermeiro=enfermeiro,
            lista_chamada_solicitacao=solicitacao,
            unidade_saude=unidade_saude,
            defaults={'arquivo': arquivo},
        )

        listagem_medicamentos = request.data.get("listagem_medicamentos")
        if isinstance(listagem_medicamentos, str):
            listagem_medicamentos = json.loads(listagem_medicamentos)

        if isinstance(listagem_medicamentos, list):
            for medicamento in listagem_medicamentos:
                medicamento_obj = Medicamento.objects.get(id=medicamento['medicacaoId'])
                
                administracao_medicamento = AdministracaoMedicamento.objects.create(
                    receita_medicamento=receita_medicamento,
                    medicacao=medicamento_obj,
                    dosagem=medicamento['dosagem'],
                    admin_medicamentosa=medicamento['medicamentosa'],
                    tipo_parenteral=medicamento['parental'],
                    quantidade=medicamento['quantidade'],
                    periodo=medicamento['periodo'],
                    posologia=medicamento['posologia'],
                    observacao=medicamento['observacao'],
                )
                
                total_aplicacoes = int(medicamento['total_aplicacoes'])
                
                for i in range(total_aplicacoes):
                    SituacaoAdministracaoMedicamento.objects.create(
                        administracao_medicamento=administracao_medicamento,
                        sequencial=i+1,
                    )

        solicitacao.situacao = ListaChamadoAdministracaoMedicamento.EM_ATENDIMENTO
        solicitacao.save()

        return Response(status=status.HTTP_201_CREATED)
    
class ReceitaMedicamentoAPIView(APIView):
    def get(self, request, format=None):
        receita_id = request.query_params.get('receita_id')
        
        receita = ReceitaMedicamento.objects.get(id=receita_id)
        receita_serializada = ReceitaMedicamentoSerializer(receita, many=False)
        
        return Response(status=status.HTTP_200_OK, data={"receita": receita_serializada.data}, content_type="application/json")
    
class SituacaoAdministracaoMedicamentoAPIView(APIView):
    def get(self, request, format=None):
        administracao_medicamento_id = request.query_params.get('administracao_medicamento_id')
        
        situacao_administracao_medicamento = SituacaoAdministracaoMedicamento.objects.filter(administracao_medicamento__id=administracao_medicamento_id).order_by('sequencial')
       
        serializer = SituacaoAdministracaoMedicamentoSerializer(situacao_administracao_medicamento, many=True)
        return Response(serializer.data)
    
    def put(self, request, format=None):
        id = request.data.get('id')

        try:
            situacao_admin_medicamento = SituacaoAdministracaoMedicamento.objects.get(id=id)

            enfermeiro_id = request.data.get('enfermeiro')
            situacao = request.data.get('situacao')
            observacao = request.data.get('observacao')
            cancelou = request.data.get('cancelou')
            aplicou_antes = request.data.get('aplicou_antes')

            if enfermeiro_id:
                
                enfermeiro = Profissional.objects.get(id=enfermeiro_id)
                situacao_admin_medicamento.enfermeiro = enfermeiro

            if situacao:
                situacao_admin_medicamento.situacao = situacao

            if observacao:
                situacao_admin_medicamento.observacao = observacao
            
            if cancelou:
                situacao_admin_medicamento.cancelou = True

            if aplicou_antes:
                situacao_admin_medicamento.aplicou_antes = True

            situacao_admin_medicamento.data_hora_aplicacao = timezone.now()
            situacao_admin_medicamento.save()

            return Response({'message': 'Atualização bem-sucedida', 'data': SituacaoAdministracaoMedicamentoSerializer(situacao_admin_medicamento).data}, status=status.HTTP_200_OK)

        except AdministracaoMedicamento.DoesNotExist:
            return Response({'error': 'Administração de medicamento não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
class FinalizarSituacaoAdministracaoMedicamentoVacinaAPIView(UpdateAPIView):
    queryset = ListaChamadoAdministracaoMedicamento.objects.all()
    serializer_class = ListaChamadoAdministracaoMedicamentoSerializer
    authentication_classes = (CsrfSessionAuthentication,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        situacao = request.data.get('situacao')

        instance.situacao = int(situacao)
        instance.save()

        instance.boletim.situacao = BoletimPaciente.ENCERRADO_SISTEMA
        instance.boletim.save()

        serializer = self.get_serializer(instance)
        return Response({'message': 'Atualização bem-sucedida', 'data': serializer.data}, status=status.HTTP_200_OK)

class ReceitaProcedimentoCreateAPIView(CreateAPIView):
    queryset = ReceitaAdministracaoProcedimento.objects.all()

    def create(self, request, *args, **kwargs):
        solicitacao_id = request.data.get("solicitacao_id")
        paciente_id = request.data.get("paciente_id")
        enfermeiro_id = request.data.get("enfermeiro_id")
        unidade_saude_id = request.data.get("unidade_saude_id")
        listagem_procedimentos = request.data.get("listagem_procedimentos")
        arquivo = request.FILES.get('file')
       
        paciente = Paciente.objects.get(id=paciente_id)
        enfermeiro = Profissional.objects.get(id=enfermeiro_id)
        unidade_saude = UnidadeSaude.objects.get(id=unidade_saude_id)
        solicitacao = ListaChamadoAdministracaoProcedimento.objects.get(id=solicitacao_id)
       
        receita_procedimento, created = ReceitaAdministracaoProcedimento.objects.get_or_create(
            paciente=paciente,
            enfermeiro=enfermeiro,
            lista_chamada_solicitacao=solicitacao,
            unidade_saude=unidade_saude,
            defaults={'arquivo': arquivo},
        )

        listagem_procedimentos = request.data.get("listagem_procedimentos")
        if isinstance(listagem_procedimentos, str):
            listagem_procedimentos = json.loads(listagem_procedimentos)

        if not listagem_procedimentos:
            return Response({"error": "A lista de procedimentos não pode estar vazia."}, status=status.HTTP_400_BAD_REQUEST)

        if isinstance(listagem_procedimentos, list):
            for procedimento in listagem_procedimentos:
                
                try:
                    procedimento_obj = Procedimento.objects.get(id=procedimento['procedimentoId'])
                except Procedimento.DoesNotExist:
                    return Response({"error": "Procedimento não encontrado"}, status=status.HTTP_400_BAD_REQUEST)
                
                administracao_procedimento = AdministracaoProcedimento.objects.create(
                    receita_procedimento=receita_procedimento,
                    procedimento=procedimento_obj,
                    quantidade=procedimento['quantidade'],
                    justificativa=procedimento['justificativa'],
                    observacao=procedimento['observacao'],
                )
                
                SituacaoAdministracaoProcedimento.objects.create(
                    administracao_procedimento=administracao_procedimento,
                    sequencial=1,
                )

        solicitacao.situacao = ListaChamadoAdministracaoProcedimento.EM_ESPERA
        solicitacao.save()

        return Response(status=status.HTTP_201_CREATED)

class SolicitacoesAdministracaoProcedimentoViewSet(viewsets.ViewSet):
    authentication_classes = (CsrfSessionAuthentication, )
    pagination_class = SimpleAPIPagination
    
    def list(self, request):
        receita_id = request.GET.get("receita_id")
        
        queryset = AdministracaoProcedimento.objects.filter(
            receita_procedimento=receita_id,
            receita_procedimento__unidade_saude=request.user.get_unidade_login().unidade
        )
        
        serializer = SolicitacaoAdministracaoProcedimentoSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET', 'PUT'])
    def lista_procedimentos_detail(self, request, pk=None):

        if request.method == 'GET':
            try:
                admin_procedimento = AdministracaoProcedimento.objects.get(id=pk)
                print(f"########## api/view/lista_procedimentos_detail/resultado: {admin_procedimento}")
            except AdministracaoProcedimento.DoesNotExist:
                return Response({'detail': 'Administração de Procedimento não encontrado'}, status=status.HTTP_404_NOT_FOUND)

            serializer = SolicitacaoAdministracaoProcedimentoSerializer(admin_procedimento)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['PUT'])
    def atualiza_procedimento_eletivo(self, request, pk=None):
        if request.method == 'PUT':
            idAdminProcedimento = request.data.get('idAdminProcedimento', '')
            idProcedimento = request.data.get('idProcedimento', '')
            text = request.data.get('text', '')
            quantidade = request.data.get('quantidade', '')
            justificativa = request.data.get('justificativa', '')
            observacao = request.data.get('observacao', '')

            try:
                instance = AdministracaoProcedimento.objects.get(id=pk)

                instance.procedimento = Procedimento.objects.get(id=idProcedimento)
                instance.quantidade = quantidade
                instance.justificativa = justificativa
                instance.observacao = observacao
                instance.save()

                return Response(SolicitacaoAdministracaoProcedimentoSerializer(instance=instance).data)
            except SolicitacaoAdministracaoProcedimentoSerializer.DoesNotExist:
                return Response({"error": "Objeto não encontrado"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['GET', 'PUT'])
    def lista_solicitacao_procedimentos_eletivo(self, request, pk=None):

        if request.method == 'GET':
            lista_chamada_solicitacao = ListaChamadoAdministracaoProcedimento.objects.get(id=pk)
            receita = ReceitaAdministracaoProcedimento.objects.get(lista_chamada_solicitacao=lista_chamada_solicitacao, lista_chamada_solicitacao__situacao=ListaChamadoAdministracaoProcedimento.EM_ATENDIMENTO)
            procedimento = AdministracaoProcedimento.objects.filter(receita_procedimento=receita)

            return Response(SolicitacaoAdministracaoProcedimentoSerializer(instance=procedimento, many=True).data)

    @action(detail=True, methods=['PUT'])
    def atualizar_situacao(self, request, pk=None):
        if request.method == 'PUT':
            situacao = request.data.get('situacao', '')
            justificativa = request.data.get('justificativa', None)
            enfermeiro = self.request.user.profissional_set.first()

            try:
                admin_procedimento = AdministracaoProcedimento.objects.get(id=pk)
                instance = SituacaoAdministracaoProcedimento.objects.get(administracao_procedimento=admin_procedimento)

                if situacao == 'suspender':
                    instance.justificativa = justificativa
                    instance.cancelou = True
                    instance.situacao = SituacaoAdministracaoProcedimento.CANCELADO
                else:
                    instance.justificativa = None
                    instance.situacao = SituacaoAdministracaoProcedimento.REALIZADO

                instance.data_hora_execucao = timezone.now()
                instance.enfermeiro = enfermeiro
                instance.save()

                return Response(SituacaoAdministracaoProcedimentoSerializer(instance=instance).data)
            except SituacaoAdministracaoProcedimento.DoesNotExist:
                return Response({"error": "Objeto não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
    # Finalizar Processo
    @action(detail=True, methods=['PUT'])
    def finalizar_atendimento(self, request, pk=None):
        solicitacao_pk = request.data.get('solicitacao_pk')

        if not solicitacao_pk:
            return Response({'error': 'solicitacao_pk é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
        
        chamada_solicitacao = get_object_or_404(ListaChamadoAdministracaoProcedimento, pk=solicitacao_pk)
        chamada_solicitacao.situacao = 4
        chamada_solicitacao.save()

        boletim = chamada_solicitacao.classificacao_risco.boletim 
        boletim.situacao = 10
        boletim.save()

        return Response({'info': 'Atendimento finalizado com sucesso'}, status=status.HTTP_200_OK)
