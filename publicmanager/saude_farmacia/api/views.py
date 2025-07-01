from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from publicmanager.saude_farmacia.models import Insumo, Medicamento, PrincipioAtivo, Produto
from .serializers import InsumoSerializer, MedicacoesSerializer, MedicamentoSerializer, PrincipioAtivoSerializer, ProdutoMedicoSerializer

class PrincipioAtivoAPIView(APIView):
    def get(self, request):
        search = request.query_params.get('search', '')
        resultados = PrincipioAtivo.objects.filter(nome__icontains=search).order_by('nome')[:30]
        serializer = PrincipioAtivoSerializer(resultados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MedicacoesAPIView(APIView):
    def get(self, request):
        search = request.query_params.get('search', '')
        unidade_saude_id = request.query_params.get('unidade_saude_id', '')

        resultados = Medicamento.objects.filter(unidade_saude=unidade_saude_id, nome_medicamento__icontains=search).order_by('nome_medicamento')[:20]
        serializer = MedicacoesSerializer(resultados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProdutoMedicoDetalheAPIView(APIView):
    def get(self, request):
        produto_id = request.query_params.get('produto_id', '')
        resultado = Produto.objects.get(id=produto_id)
        if resultado is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProdutoMedicoSerializer(resultado)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MedicamentoDetalheAPIView(APIView):
    def get(self, request):
        medicamento_id = request.query_params.get('medicamento_id', '')
        resultado = Medicamento.objects.get(id=medicamento_id)
        if resultado is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MedicamentoSerializer(resultado)
        return Response(serializer.data, status=status.HTTP_200_OK)

class InsumoDetalheAPIView(APIView):
    def get(self, request):
        insumo_id = request.query_params.get('insumo_id', '')
        resultado = Insumo.objects.get(id=insumo_id)
        if resultado is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = InsumoSerializer(resultado)
        return Response(serializer.data, status=status.HTTP_200_OK)
