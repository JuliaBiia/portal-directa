from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response 
from django.db.models import Value, CharField
from django.contrib.auth.mixins import LoginRequiredMixin

from publicmanager.saude_cadastro.models import PainelChamada
from publicmanager.saude_atendimento.models import ListaChamada, ListaChamadaClassificacaoRisco
from publicmanager.saude_enfermagem.models import ListaChamadaSolicitacaoAtendimento, ListaChamadoAdministracaoMedicamento
    
class SaudePainelChamadaDetailAPIView(LoginRequiredMixin, APIView):

    def get(self, request, *args, **kwargs):
        slug = self.request.GET.get('slug')
        setores = PainelChamada.objects.filter(unidade_saude=kwargs.get('pk'), slug=slug).values_list('setores__pk')

        lista_chamada_classificacao_risco = ListaChamadaClassificacaoRisco.objects.filter(
            sala__unidade_setor__pk__in=setores,
            situacao__in=[ListaChamadaClassificacaoRisco.CHAMADO, ListaChamadaClassificacaoRisco.EM_ATENDIMENTO, ListaChamadaClassificacaoRisco.CLASSIFICADO],
        ).order_by('-updated_at').values_list(
            'sala__nome_sala', 'unidade_saude', 'boletim__paciente__nome_paciente', 'contagem', 'profissional__nome_profissional', 
            'sala__unidade_setor__tipo', Value(None, output_field=CharField()), 'updated_at')

        listagem_chamadas_urgencia = ListaChamada.objects.filter(
            sala__unidade_setor__pk__in=setores,
            situacao__in=[ListaChamada.EM_ESPERA, ListaChamada.EM_PROCEDIMENTO, ListaChamada.RETORNO, ListaChamada.EM_ATENDIMENTO_RETORNO],
        ).order_by('-updated_at').values_list(
            'sala__nome_sala', 'unidade_saude', 'paciente__nome_paciente', 'contagem', 'medico__nome_profissional', 
            'sala__unidade_setor__tipo', 'classificacao_risco__tipo_classificacao_risco__cor', 'updated_at')

        listagem_chamadas_enfermagem = ListaChamadaSolicitacaoAtendimento.objects.filter(
            sala__unidade_setor__pk__in=setores,
            situacao__in=[ListaChamadaSolicitacaoAtendimento.DESIGNADO, ListaChamadaSolicitacaoAtendimento.EM_ATENDIMENTO]
        ).order_by('-updated_at').values_list(
            'sala__nome_sala', 'unidade_saude', 'atendimento__paciente__nome_paciente', 'contagem', 'enfermeiro__nome_profissional',
            'sala__unidade_setor__tipo', 'atendimento__classificacao_risco__tipo_classificacao_risco__cor', 'updated_at')
        listagem_administracao_medicacao = ListaChamadoAdministracaoMedicamento.objects.filter(
            sala__unidade_setor__pk__in=setores,
            situacao__in=[ListaChamadoAdministracaoMedicamento.DESIGNADO, ListaChamadoAdministracaoMedicamento.EM_ATENDIMENTO]
        ).order_by('-updated_at').values_list(
            'sala__nome_sala', 'unidade_saude', 'boletim__paciente__nome_paciente', 'contagem', 'enfermeiro__nome_profissional',
            'sala__unidade_setor__tipo', Value(None, output_field=CharField()), 'updated_at')
        
        listagem_chamadas = sorted(list(lista_chamada_classificacao_risco) + list(listagem_chamadas_urgencia) + list(listagem_chamadas_enfermagem) + list(listagem_administracao_medicacao), key=lambda x: x[7], reverse=True)

        chamadas_unicas = {}
        for chamada in listagem_chamadas:
            nome_paciente = chamada[2]
            if nome_paciente not in chamadas_unicas:
                chamadas_unicas[nome_paciente] = chamada

        chamadas_serializadas = []
        for chamada in chamadas_unicas.values():

            setor_nome = None
            if chamada[5] == 0:
                setor_nome = 'RECEPÇÃO'
            elif chamada[5] == 1:
                setor_nome = 'URGÊNCIA'
            elif chamada[5] == 2:
                setor_nome = 'CONSULTÓRIO'
            elif chamada[5] == 3:
                setor_nome = 'ENFERMARIA'
            elif chamada[5] == 4:
                setor_nome = 'INTERNAÇÃO'
            elif chamada[5] == 5:
                setor_nome = 'FARMACIA'
            elif chamada[5] == 6:
                setor_nome = 'NUTRIÇÃO'
            elif chamada[5] == 7:
                setor_nome = 'LABORATÓRIO'
            elif chamada[5] == 8:
                setor_nome = 'CENTRO CIRÚRGICO'
            elif chamada[5] == 9:
                setor_nome = 'MATERNIDADE'
            elif chamada[5] == 10:
                setor_nome = 'OBSTRETICIA'
            elif chamada[5] == 11:
                setor_nome = 'PEDIATRIA'
            elif chamada[5] == 12:
                setor_nome = 'RADIOLOGIA'
            elif chamada[5] == 13:
                setor_nome = 'RH'
            elif chamada[5] == 14:
                setor_nome = 'ADMINISTRATIVO'
            elif chamada[5] == 15:
                setor_nome = 'CLASSIFICAÇÃO DE RISCO'

            chamada_dict = {
                'sala_nome': chamada[0],
                'unidade_saude': chamada[1],
                'paciente_nome': chamada[2],
                'contagem': chamada[3],
                'profissional_nome': chamada[4],
                'setor_nome': setor_nome,
                'classicicacao_cor': chamada[6],
                'updated_at': chamada[7],
            }
            chamadas_serializadas.append(chamada_dict)

        chamadas_serializadas = chamadas_serializadas[:10]

        return Response(chamadas_serializadas, status=status.HTTP_200_OK)