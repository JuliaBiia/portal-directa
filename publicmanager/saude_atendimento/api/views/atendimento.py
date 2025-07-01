from django.urls import reverse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from publicmanager.saude_enfermagem.models import ListaChamadaSolicitacaoAtendimento, ListaChamadoAdministracaoProcedimento
from publicmanager.saude_atendimento.api.serializers.atendimento import RastrearPacienteSerializer
from publicmanager.saude_atendimento.models import  BoletimPaciente, AtendimentoMedico, ListaChamada, ClassificacaoRisco, ListaChamadaClassificacaoRisco

class RastrearPacientesAPIView(APIView):
    def get_url_by_tipo(self, tipo):
        if tipo == ListaChamadaSolicitacaoAtendimento.EXAME_LABORATORIO:
            return reverse('saude_enfermagem:exames_laboratoriais_list')
        elif tipo == ListaChamadaSolicitacaoAtendimento.EXAME_IMAGEM:
            return reverse('saude_enfermagem:exames_imagem_list')
        elif tipo == ListaChamadaSolicitacaoAtendimento.PROCEDIMENTO:
            return reverse('saude_enfermagem:procedimentos_list')
        elif tipo == ListaChamadaSolicitacaoAtendimento.MEDICACAO:
            return reverse('saude_enfermagem:administracao_medicacao_list')
        return None
    
    def get(self, request):
        unidade_saude_id = request.query_params.get('unidade_saude_id', '')
        paciente_nome = request.query_params.get('paciente_nome', '')
        local_tag = request.query_params.get('local', '')

        boletins_paciente = BoletimPaciente.objects.filter(
            unidade_saude=unidade_saude_id,
            situacao__in=[BoletimPaciente.EM_ABERTO, BoletimPaciente.EM_ANDAMENTO]
        ).order_by('paciente', '-created_at').distinct('paciente')

        lista_pacientes = []
        for boletim in boletins_paciente:
            atendimento_medico = AtendimentoMedico.objects.filter(classificacao_risco__boletim=boletim).first()
            lista_chamada = ListaChamada.objects.filter(classificacao_risco__boletim=boletim).first()
            classificacao_risco = ClassificacaoRisco.objects.filter(boletim=boletim).first()
            procedimento_eletivo = ListaChamadoAdministracaoProcedimento.objects.filter(classificacao_risco__boletim=boletim).first()

            if procedimento_eletivo and self.request.user.tipo_usuario in ['medico', 'enfermeiro', 'tecnico_enfermagem', 'desenvolvedor']:
                lista_pacientes.append({
                    'boletim_id': boletim.id,
                    'paciente': boletim.paciente.nome_paciente.upper(),
                    'local': 'PROCEDIMENTO AMBULATORIAL',
                    'local_tag': 'procedimento_eletivo',
                    'situacao': 'PROCEDIMENTO AMBULATORIAL',
                    'data_hora_entrada': procedimento_eletivo.classificacao_risco.boletim.created_at,
                    'url': reverse('saude_enfermagem:procedimentos_list'),
                })

            elif atendimento_medico:
                lista_chamada_solicitacao_atendimento = ListaChamadaSolicitacaoAtendimento.objects.filter(
                    atendimento=atendimento_medico,
                    situacao__in=[
                        ListaChamadaSolicitacaoAtendimento.EM_ESPERA, 
                        ListaChamadaSolicitacaoAtendimento.DESIGNADO, 
                        ListaChamadaSolicitacaoAtendimento.EM_ATENDIMENTO
                    ]
                ).first()
                
                if lista_chamada_solicitacao_atendimento and self.request.user.tipo_usuario in ['enfermeiro', 'tecnico_enfermagem', 'desenvolvedor']:
                    url = self.get_url_by_tipo(lista_chamada_solicitacao_atendimento.tipo)
                        
                    lista_pacientes.append({
                        'boletim_id': lista_chamada_solicitacao_atendimento.atendimento.lista_chamada.classificacao_risco.boletim.id,
                        'paciente': lista_chamada_solicitacao_atendimento.atendimento.lista_chamada.classificacao_risco.boletim.paciente.nome_paciente.upper(),
                        'local': f'ENFERMAGEM {lista_chamada_solicitacao_atendimento.get_tipo_display().upper()}',
                        'local_tag': f'enfermagem_{lista_chamada_solicitacao_atendimento.tipo}',
                        'situacao': lista_chamada_solicitacao_atendimento.get_situacao_display().upper(),
                        'data_hora_entrada': lista_chamada_solicitacao_atendimento.created_at,
                        'url': url,
                    })
                elif self.request.user.tipo_usuario in ['medico', 'enfermeiro', 'tecnico_enfermagem', 'desenvolvedor']:
                    
                    if self.request.user.tipo_usuario == 'medico' and atendimento_medico.lista_chamada.situacao in [ListaChamada.EM_ESPERA, ListaChamada.EM_ATENDIMENTO, ListaChamada.LISTA_RETORNO, ListaChamada.RETORNO, ListaChamada.EM_ATENDIMENTO_RETORNO]:
                        
                        situacao = 'em_atendimento'
                        if atendimento_medico.lista_chamada.situacao == ListaChamada.EM_ESPERA:
                            situacao = 'em_espera'
                        elif atendimento_medico.lista_chamada.situacao == ListaChamada.EM_ATENDIMENTO:
                            situacao = 'em_atendimento'
                        elif atendimento_medico.lista_chamada.situacao == ListaChamada.LISTA_RETORNO:
                            situacao = 'lista_retorno'
                        elif atendimento_medico.lista_chamada.situacao == ListaChamada.RETORNO:
                            situacao = 'retorno'
                        elif atendimento_medico.lista_chamada.situacao == ListaChamada.EM_ATENDIMENTO_RETORNO:
                            situacao = 'em_atendimento_retorno'

                        lista_pacientes.append({
                            'boletim_id': boletim.id,
                            'paciente': boletim.paciente.nome_paciente.upper(),
                            'local': 'ATENDIMENTO MÉDICO',
                            'local_tag': 'atendimento',
                            'situacao': situacao,
                            'data_hora_entrada': atendimento_medico.created_at,
                            'url': reverse('saude_atendimento:atendimento_medico_list'),
                        })
                    elif self.request.user.tipo_usuario in ['enfermeiro', 'tecnico_enfermagem', 'desenvolvedor']:
                        lista_pacientes.append({
                            'boletim_id': boletim.id,
                            'paciente': boletim.paciente.nome_paciente.upper(),
                            'local': 'ATENDIMENTO MÉDICO',
                            'local_tag': 'atendimento',
                            'situacao': 'em_atendimento',
                            'data_hora_entrada': atendimento_medico.created_at,
                            'url': reverse('saude_atendimento:atendimento_medico_list'),
                        })

            elif lista_chamada and self.request.user.tipo_usuario in ['medico', 'enfermeiro', 'tecnico_enfermagem', 'desenvolvedor']:
                
                lista_pacientes.append({
                    'boletim_id': boletim.id,
                    'paciente': boletim.paciente.nome_paciente.upper(),
                    'local': 'ATENDIMENTO MÉDICO',
                    'local_tag': 'atendimento',
                    'situacao': 'espera_chamada_atendimento',
                    'data_hora_entrada': lista_chamada.created_at,
                    'url': reverse('saude_atendimento:atendimento_medico_list'),
                })

            elif classificacao_risco and self.request.user.tipo_usuario in ['medico', 'enfermeiro', 'tecnico_enfermagem', 'desenvolvedor']:
                
                if lista_chamada and self.request.user.tipo_usuario == 'medico':
                    lista_pacientes.append({
                        'boletim_id': boletim.id,
                        'paciente': boletim.paciente.nome_paciente.upper(),
                        'local': 'ATENDIMENTO MÉDICO',
                        'local_tag': 'atendimento',
                        'situacao': 'lista_chamada',
                        'data_hora_entrada': classificacao_risco.created_at,
                        'url': reverse('saude_atendimento:atendimento_medico_list'),
                    })
                elif not lista_chamada and self.request.user.tipo_usuario in ['enfermeiro', 'tecnico_enfermagem', 'desenvolvedor']:
                    lista_pacientes.append({
                        'boletim_id': boletim.id,
                        'paciente': boletim.paciente.nome_paciente.upper(),
                        'local': 'ATENDIMENTO MÉDICO',
                        'local_tag': 'atendimento',
                        'situacao': 'lista_chamada',
                        'data_hora_entrada': classificacao_risco.created_at,
                        'url': reverse('saude_atendimento:atendimento_medico_list'),
                    })

            elif boletim.tipo == BoletimPaciente.URGENCIA and self.request.user.tipo_usuario in ['enfermeiro', 'tecnico_enfermagem', 'desenvolvedor']:
                lista_classificacao = ListaChamadaClassificacaoRisco.objects.filter(
                    boletim=boletim, situacao=ListaChamadaClassificacaoRisco.CLASSIFICADO
                ).first()

                if not lista_classificacao:
                    lista_pacientes.append({
                        'boletim_id': boletim.id,
                        'paciente': boletim.paciente.nome_paciente.upper(),
                        'local': 'AGUARDANDO CLASSIFICAÇÃO DE RISCO',
                        'local_tag': 'classificacao_risco',
                        'situacao': 'classificacao_risco',
                        'data_hora_entrada': boletim.created_at,
                        'url': reverse('saude_atendimento:classificacao_risco_list'),
                    })

            elif boletim.tipo == BoletimPaciente.MEDICACAO and self.request.user.tipo_usuario in ['medico', 'enfermeiro', 'tecnico_enfermagem', 'desenvolvedor']:
                lista_pacientes.append({
                    'boletim_id': boletim.id,
                    'paciente': boletim.paciente.nome_paciente.upper(),
                    'local': 'MEDICAÇÃO E VACINA',
                    'local_tag': 'medicacao_vacina',
                    'situacao': 'medicacao_vacina',
                    'data_hora_entrada': boletim.created_at,
                    'url': reverse('saude_enfermagem:administracao_medicamento_vacina_aberto_list'),
                })

        lista_chamada_solicitacao = ListaChamadaSolicitacaoAtendimento.objects.exclude(
            atendimento__lista_chamada__classificacao_risco__boletim__in=[
                BoletimPaciente.EM_ABERTO, 
                BoletimPaciente.EM_ANDAMENTO
            ],
        ).filter(
            situacao__in=[ListaChamadaSolicitacaoAtendimento.EM_ESPERA, 
                ListaChamadaSolicitacaoAtendimento.DESIGNADO, 
                ListaChamadaSolicitacaoAtendimento.EM_ATENDIMENTO
            ],
            atendimento__lista_chamada__situacao__in=[
                ListaChamada.ENCERRADO_ATENDIMENTO, 
                ListaChamada.ENCERRADO_ALTA, 
                ListaChamada.ENCERRADO_RECEPCAO,
                ListaChamada.ENCERRADO_SISTEMA
            ]
        )

        if lista_chamada_solicitacao and self.request.user.tipo_usuario in ['enfermeiro', 'tecnico_enfermagem', 'desenvolvedor']:
            for lista in lista_chamada_solicitacao:
                url = self.get_url_by_tipo(lista.tipo)

                lista_pacientes.append({
                    'boletim_id': lista.atendimento.lista_chamada.classificacao_risco.boletim.id,
                    'paciente': lista.atendimento.lista_chamada.classificacao_risco.boletim.paciente.nome_paciente.upper(),
                    'local': f'ENFERMAGEM {lista.get_tipo_display().upper()}',
                    'local_tag': f'enfermagem_{lista.tipo}',
                    'situacao': lista.get_situacao_display().upper(),
                    'data_hora_entrada': lista.created_at,
                    'url': url,
                })

        # Ordenando a lista de pacientes 
        lista_pacientes = sorted(lista_pacientes, key=lambda x: x['data_hora_entrada'], reverse=True)

        if paciente_nome:
            lista_pacientes = [
                paciente for paciente in lista_pacientes
                if paciente_nome.upper() in paciente['paciente']
            ]

        if local_tag:
            lista_pacientes = [
                paciente for paciente in lista_pacientes
                if local_tag in paciente['local_tag']
            ]

        serializer = RastrearPacienteSerializer(lista_pacientes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)