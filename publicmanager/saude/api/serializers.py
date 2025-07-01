from rest_framework import serializers
from publicmanager.saude.models import UnidadeLogin

class AtualizarUnidadeLoginSerializer(serializers.ModelSerializer):
        setor_tipo = serializers.SerializerMethodField()

        class Meta:
                model = UnidadeLogin
                fields = ('sala', 'setor_tipo')

        def get_setor_tipo(self, obj):
                if obj.sala:
                        return obj.sala.unidade_setor.tipo
                return None

