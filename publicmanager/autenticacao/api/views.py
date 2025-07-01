from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import UnidadeSaudeSerializer
from publicmanager.saude_cadastro.models import Profissional
from publicmanager.saude.models import UnidadeSaude, UnidadeLogin

class UnidadesPorCpfAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        cpf = request.GET.get('cpf')

        try:
            profissional = Profissional.objects.get(user__cpf_cnpj=cpf)

            unidade_login = UnidadeLogin.objects.filter(profissional=profissional).first()

            unidades = list(profissional.unidades_saude.all())

            if unidade_login and unidade_login.unidade in unidades:
                unidades.remove(unidade_login.unidade)
                unidades.insert(0, unidade_login.unidade)

            serializer = UnidadeSaudeSerializer(unidades, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profissional.DoesNotExist:
            return Response({'error': 'Sem conteúdo'}, status=status.HTTP_204_NO_CONTENT)