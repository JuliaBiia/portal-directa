from django import forms
from publicmanager.saude.models import EsqueceuSenha
class SaudeLoginForm(forms.Form):
    cpf = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)
    unidades = forms.CharField()


class AlterarSenhaCriarForm(forms.ModelForm):
      class Meta:
        model = EsqueceuSenha
        fields = ('email', 'whatsapp')