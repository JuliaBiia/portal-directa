from rest_framework import serializers
from publicmanager.saude_farmacia.models import Insumo, Medicamento, PrincipioAtivo, Produto

class PrincipioAtivoSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()

    class Meta:
        model = PrincipioAtivo
        fields = ('value', 'text')

    def get_value(self, obj):
        return obj.id
    
    def get_text(self, obj):
        return obj.nome
        

class MedicacoesSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()

    class Meta:
        model = Medicamento
        fields = ('value', 'text', 'quantidade')

    def get_value(self, obj):
        return obj.id
    
    def get_text(self, obj):
        return obj.nome_medicamento

class ProdutoMedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ('id','codigo_de_barra')

class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = ('id','codigo_de_barra')

class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = ('id','codigo_de_barra')
