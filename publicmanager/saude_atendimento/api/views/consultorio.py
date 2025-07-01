import datetime
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError

from publicmanager.saude_atendimento.api.serializers.consultorio import (
    AgendamentoCreateSerializer, BloqueioAgendaSerializer, FeriadoSerializer, 
    AgendamentoConsultorioSerializer
)
from publicmanager.saude_atendimento.models import (
    BloqueioAgenda, Feriado, AgendamentoConsultorio, Profissional
)


class ObterQuantidadeDeAtendimentosDoMedicoPorTipoEmDeterminadaData(generics.ListAPIView):
    def get(self, request):
        medico_id = request.query_params.get('medico_id', '')
        data_atendimento = request.query_params.get('data_atendimento', '')

        [ ano, mes, dia ] = data_atendimento.split("-")

        data_atendimento = datetime.date(int(ano), int(mes), int(dia))

        atendimento_tipo_primeiro_atendimento = AgendamentoConsultorio.objects.filter(
            medico__id__exact=medico_id,
            data_atendimento=data_atendimento,
            tipo_atendimento__exact=0
        )
        atendimento_tipo_extra_encaixe = AgendamentoConsultorio.objects.filter(
            medico__id__exact=medico_id,
            data_atendimento=data_atendimento,
            tipo_atendimento__exact=1
        )
        atendimento_tipo_retorno = AgendamentoConsultorio.objects.filter(
            medico__id__exact=medico_id,
            data_atendimento=data_atendimento,
            tipo_atendimento__exact=2
        )

        return Response([len(atendimento_tipo_primeiro_atendimento), len(atendimento_tipo_extra_encaixe), len(atendimento_tipo_retorno)])

class AgendamentoConsultorioListAPIView(generics.ListAPIView):
    queryset = AgendamentoConsultorio.objects.all()
    serializer_class = AgendamentoConsultorioSerializer
    
class AgendamentoConsultorioAPICreateView(generics.CreateAPIView):
    queryset = AgendamentoConsultorio.objects.all()
    serializer_class = AgendamentoCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)       
        except DjangoValidationError as e:
            raise ValidationError(e.messages)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        serializer.save()

class DetalheAgendamentoConsultorioAPIView(APIView):

    def get_object(self, id):
        try:
            return AgendamentoConsultorio.objects.get(id=id)
        except AgendamentoConsultorio.DoesNotExist:
            return None

    def get(self, request, id, format=None):
        agendamento = self.get_object(id)
        if agendamento is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AgendamentoConsultorioSerializer(agendamento)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        agendamento = self.get_object(id)
        if agendamento is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AgendamentoConsultorioSerializer(agendamento, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return Response(serializer.data)
        except DjangoValidationError as e:
            raise ValidationError(e.messages)
    
    def delete(self, request, *args, **kwargs):
        try:
            instance = AgendamentoConsultorio.objects.get(id=kwargs["id"])
            instance.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ObterAgendamentoPorDataInicialDataFinal(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        medico_id = request.query_params.get('medico_id', '')
        data_inicial = request.query_params.get('data_inicial', '')
        data_final = request.query_params.get('data_final', '')

        agendamentos = AgendamentoConsultorio.objects.filter(
            medico__id__exact=medico_id,
            data_atendimento__gte=data_inicial,
        ).filter(
            data_atendimento__lte=data_final
        )
        
        if agendamentos:
            serializer = AgendamentoConsultorioSerializer(agendamentos, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class FeriadoCreateView(generics.CreateAPIView):
    queryset = Feriado.objects.all()
    serializer_class = FeriadoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)       
        except DjangoValidationError as e:
            raise ValidationError(e.messages)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class FeriadoUpdateView(generics.UpdateAPIView):
    queryset = Feriado.objects.all()
    serializer_class = FeriadoSerializer

    def update(self, request, *args, **kwargs):
        feriado = Feriado.objects.get(id=kwargs["id"])

        serializer = self.get_serializer(instance=feriado, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer)       
        except DjangoValidationError as e:
            raise ValidationError(e.messages)
        self.perform_update(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()

class FeriadoDeleteView(generics.DestroyAPIView):
    queryset = Feriado.objects.all()
    serializer_class = FeriadoSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = Feriado.objects.get(id=kwargs["id"])
            instance.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BloqueioAgendaCreateView(generics.CreateAPIView):
    queryset = BloqueioAgenda.objects.all()
    serializer_class = BloqueioAgendaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)       
        except DjangoValidationError as e:
            raise ValidationError(e.messages)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        medico = Profissional.objects.get(id=self.request.data["medico"])
        serializer.save(medico=medico)

class BloqueioAgendaUpdateView(generics.UpdateAPIView):
    queryset = BloqueioAgenda.objects.all()
    serializer_class = BloqueioAgendaSerializer

    def update(self, request, *args, **kwargs):
        bloqueio_agenda = BloqueioAgenda.objects.get(id=kwargs["id"])

        serializer = self.get_serializer(instance=bloqueio_agenda, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer)       
        except DjangoValidationError as e:
            raise ValidationError(e.messages)
        self.perform_update(serializer)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()

class BloqueioAgendaDeleteView(generics.DestroyAPIView):
    queryset = BloqueioAgenda.objects.all()
    serializer_class = BloqueioAgendaSerializer

    def destroy(self, request, *args, **kwargs):
        try:
           
            instance = BloqueioAgenda.objects.get(id=kwargs["id"])
            instance.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
