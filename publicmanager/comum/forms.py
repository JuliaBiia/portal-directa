from django import forms
from .models import Banco, EstadoCivil, Municipio, GrupoDeficiencia, Deficiencia, Raca

class BancoForm(forms.ModelForm):
    class Meta:
        model = Banco
        fields = '__all__'


class EstadoCivilForm(forms.ModelForm):
    class Meta:
        model = EstadoCivil
        fields = '__all__'


class MunicipioForm(forms.ModelForm):
    class Meta:
        model = Municipio
        fields = '__all__'


class GrupoDeficienciaForm(forms.ModelForm):
    class Meta:
        model = GrupoDeficiencia
        fields = '__all__'


class DeficienciaForm(forms.ModelForm):
    class Meta:
        model = Deficiencia
        fields = '__all__'


class RacaForm(forms.ModelForm):
    class Meta:
        model = Raca
        fields = '__all__'