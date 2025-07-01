from dal import autocomplete
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from publicmanager.comum.utils import CsrfSessionAuthentication

from publicmanager.saude.models import UnidadeSaude
from .serializers import CidSerializer, ExameSerializer, ProcedimentoSerializer, ProfissionalSerializer
from publicmanager.saude_cadastro.models import CID, Exame, Procedimento, TipoClassificacaoRisco, Profissional


class CidAPIView(APIView):
    def get(self, request):
        search = request.query_params.get('search', '')
        resultados = CID.objects.filter(Q(nome__icontains=search) | Q(codigo__icontains=search)).order_by('nome')[:7]
        serializer = CidSerializer(resultados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CidAPIAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CID.objects.none()

        qs = CID.objects.all()

        if self.q:
            qs = qs.filter(Q(nome__icontains=self.q) | Q(codigo__icontains=self.q))

        return qs
    
    def get_result_label(self, result):
        return f"{result.codigo} - {result.nome}"

class ExameAPIView(APIView):
    def get(self, request):
        search = request.query_params.get('search', '')
        resultados = Exame.objects.filter(nome__icontains=search, removido_sistema=False).order_by('nome')[:7]
        serializer = ExameSerializer(resultados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProcedimentoAPIView(APIView):
    def get(self, request):
        search = request.query_params.get('search', '')
        resultados = Procedimento.objects.filter(Q(nome__icontains=search) | Q(codigo__icontains=search)).order_by('nome')[:7]
        serializer = ProcedimentoSerializer(resultados, many=True)
        print(f"Valor de pesquisa3: {serializer}")

        return Response(serializer.data, status=status.HTTP_200_OK)

class ProcedimentoDetailAPIView(APIView):
    def get(self, request, pk):
        print(f"aaaaaaaaaaaaaaaaaaaaaaaa: {pk}")
        try:
            procedimento = Procedimento.objects.get(id=pk)
            print(f"bbbbbbbbbbbbbbbbbbbbbbbbb: {procedimento}")
        except Procedimento.DoesNotExist:
            return Response({'detail': 'Procedimento não encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProcedimentoSerializer(procedimento)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TipoClassificacaoRiscoUpdateAPIView(UpdateAPIView):
    queryset = TipoClassificacaoRisco.objects.all()
    authentication_classes = (CsrfSessionAuthentication, )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        situacao = request.data.get('situacao', '')
        tempo_atendimento = request.data.get('tempo_atendimento', '')

        instance.situacao = int(situacao)
        instance.tempo_atendimento = tempo_atendimento
        instance.save()

        return Response(status=status.HTTP_200_OK)
    
class ProfissionalAPIView(APIView):
    def get(self, request):
        unidade_saude_id = request.query_params.get('unidade_saude_id', '')
        tipo = request.query_params.get('tipo', '')
        unidade_saude = UnidadeSaude.objects.get(id=unidade_saude_id)

        resultados = Profissional.objects.filter(
            tipo_profissional__in=[int(tipo),0],
            unidades_saude=unidade_saude
        ).order_by('nome_profissional')

        serializer = ProfissionalSerializer(resultados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  
    
class ProfissionalRecepcaoNoturnoAPIView(UpdateAPIView):
    queryset = Profissional.objects.all()
    authentication_classes = (CsrfSessionAuthentication, )

    def update(self, request, *args, **kwargs):
        profissional = Profissional.objects.get(id=kwargs['pk'])

        confirmacao_recepcao_noturna = self.request.GET.get('confirmacao_recepcao_noturna', '')
        
        if confirmacao_recepcao_noturna == 'false':
            recep_noturna = True
        else:
            recep_noturna = False

        profissional.recepcao_noturno = recep_noturna
        profissional.save()

        return Response(status=status.HTTP_200_OK)      

"""
class FinalizarBoletimAtendimentoUpdateAPIView(UpdateAPIView):
    queryset = BoletimPaciente.objects.all()
    authentication_classes = (CsrfSessionAuthentication, )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        chamado_id = request.data.get('chamado_id', '')
        chamado_situacao = request.data.get('situacao_chamado', '')
        boletim_situacao = request.data.get('situacao')

        instance.situacao = int(boletim_situacao)
        instance.data_saida = timezone.now()
        instance.save()

        if chamado_id:
            lista_chamada =  ListaChamada.objects.get(pk=chamado_id)
            lista_chamada.situacao = int(chamado_situacao)
            lista_chamada.save()

        return Response(status=status.HTTP_200_OK)
"""