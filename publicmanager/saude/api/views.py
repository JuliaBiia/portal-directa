from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView

from publicmanager.saude.models import UnidadeLogin
from publicmanager.saude_cadastro.models import Sala
from publicmanager.comum.utils import CsrfSessionAuthentication
from .serializers import AtualizarUnidadeLoginSerializer

class AtualizarUnidadeLoginAPIView(UpdateAPIView):
    serializer_class = AtualizarUnidadeLoginSerializer
    queryset = UnidadeLogin.objects.all()
    authentication_classes = (CsrfSessionAuthentication, )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        tipo = self.request.data.get('tipo')
        sala = Sala.objects.get(pk=self.request.data.get('sala_pk'))

        if tipo == 'entrar':
            instance.sala = sala
            instance.save(skip_hooks=True)

        elif tipo == 'substituir':
            login = UnidadeLogin.objects.get(sala=sala)
            login.sala = None
            login.save(skip_hooks=True)
       
            instance.sala = sala
            instance.save(skip_hooks=True)

        elif tipo == 'sair':
            instance.sala = None
            instance.save(skip_hooks=True)

        return Response(AtualizarUnidadeLoginSerializer(instance=instance).data)