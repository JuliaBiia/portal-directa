from datetime import date
from rest_framework import serializers
from publicmanager.saude.models import UnidadeSaude

class UnidadeSaudeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UnidadeSaude
        fields = '__all__'