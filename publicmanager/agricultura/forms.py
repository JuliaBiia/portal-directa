from django import forms
from .models import TipoProdutor


class TipoProdutorForm(forms.ModelForm):
    class Meta:
        model = TipoProdutor
        fields = '__all__'
