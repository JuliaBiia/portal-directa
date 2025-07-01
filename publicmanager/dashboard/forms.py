from django import forms

from publicmanager.autenticacao.models import Usuario
from publicmanager.saude_cadastro.models import Profissional

class MeuPerfilUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profissional
        exclude = ('user', 'unidades_saude', 'tipo_profissional', 'situacao')

    def clean_telefone_1(self):
        telefone_1 = self.cleaned_data.get('telefone_1')

        try:
            return telefone_1
        except forms.ValidationError:
            raise forms.ValidationError("Este número de telefone já está associado a uma conta existente.")

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        cpf_sem_caracteres = ''.join(filter(str.isdigit, cpf))

        if self.instance and self.instance.cpf == cpf_sem_caracteres:
            return cpf
       
        elif Usuario.objects.filter(cpf_cnpj=cpf_sem_caracteres).exists():
            raise forms.ValidationError("Este CPF já está vinculado a uma conta existente.")
        
        return cpf
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            return email
        except forms.ValidationError:
             raise forms.ValidationError("Já existe um usuário registrado com este endereço de e-mail.")
