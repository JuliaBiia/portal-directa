from rest_framework import serializers

class RastrearPacienteSerializer(serializers.Serializer):
    data_hora_entrada = serializers.DateTimeField(format="%d/%m/%Y %H:%M")
    boletim_id = serializers.UUIDField()
    paciente = serializers.CharField(max_length=255)
    local = serializers.CharField(max_length=255)
    local_tag = serializers.CharField(max_length=255)
    situacao = serializers.CharField(max_length=255)
    url = serializers.URLField()