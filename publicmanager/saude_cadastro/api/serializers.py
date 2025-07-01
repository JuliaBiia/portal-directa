from rest_framework import serializers

from publicmanager.saude_cadastro.models import Profissional
from publicmanager.saude_cadastro.models import (
    CID, Exame, Procedimento
)


class CidSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()
    codigo = serializers.SerializerMethodField()
    class Meta:
        model = CID
        fields = ('value', 'text', 'codigo')

    def get_value(self, obj):
        return obj.id
    
    def get_text(self, obj):
        return obj.nome
    
    def get_codigo(self, obj):
        return obj.codigo
    
class ExameSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()
    class Meta:
        model = Exame
        fields = ('value', 'text')

    def get_value(self, obj):
        return obj.id
    
    def get_text(self, obj):
        return obj.nome
    
class ProcedimentoSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()
    class Meta:
        model = Procedimento
        fields = ('value', 'text', 'codigo')

    def get_value(self, obj):
        return obj.id
    
    def get_text(self, obj):
        return obj.nome
    
    def get_codigo(self, obj):
        return obj.codigo
    

class ProfissionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profissional
        fields = ('id', 'nome_profissional')
