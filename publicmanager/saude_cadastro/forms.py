from django import forms

from publicmanager.comum.models import Estado
from publicmanager.autenticacao.models import Usuario
from publicmanager.saude_atendimento.models import Paciente
from .models import (
    CID, Convenio, DestinoObito, Exame, PainelChamada,
    Profissao, Sala, TipoClinica, TipoExame, TipoHistoriaClinica,
    TipoPosologia, Transporte, Profissional, UnidadeSetor
)

class TipoClinicaForm(forms.ModelForm):
    class Meta:
        model = TipoClinica
        fields = '__all__'

class ConvenioForm(forms.ModelForm):
    class Meta:
        model = Convenio
        fields = '__all__'


class CIDForm(forms.ModelForm):
    class Meta:
        model = CID
        fields = '__all__'

class CIDFilterForm(forms.ModelForm):
    codigo = forms.CharField(label='Código', max_length=20, required=False)
    nome = forms.CharField(label='Nome', max_length=200, required=False)

    class Meta:
        model = CID
        fields = '__all__'


class DestinoObitoForm(forms.ModelForm):
    class Meta:
        model = DestinoObito
        fields = '__all__'

class DestinoObitoFilterForm(forms.ModelForm):
    destino_de_obito = forms.CharField(label='Destino de Óbito', max_length=50, required=False)

    class Meta:
        model = DestinoObito
        fields = '__all__'


class TipoExameForm(forms.ModelForm):
    class Meta:
        model = TipoExame
        fields = '__all__'

class TipoExamesFilterForm(forms.ModelForm):
    destino_de_obito = forms.CharField(label='Destino de Óbito', max_length=50, required=False)

    class Meta:
        model = TipoExame
        fields = '__all__'


class ExameForm(forms.ModelForm):
    class Meta:
        model = Exame
        fields = '__all__'

class ExameFilterForm(forms.ModelForm):
    nome = forms.CharField(label='Exame', max_length=150, required=False)
    tipo_de_exames = forms.ModelChoiceField(queryset=TipoExame.objects.all(), label='Tipo de Exames', required=False)

    class Meta:
        model = Exame
        fields = ('nome', 'tipo_de_exames')

class TipoHistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = TipoHistoriaClinica
        fields = '__all__'

class TipoHistoriaClinicaFilterForm(forms.ModelForm):
    tipo_de_historia_clinica = forms.CharField(label='Tipo de história clínica', max_length=50, required=False)

    class Meta:
        model = TipoHistoriaClinica
        fields = '__all__'


class TipoPosologiaForm(forms.ModelForm):
    class Meta:
        model = TipoPosologia
        fields = '__all__'

class TipoPosologiaFilterForm(forms.ModelForm):
    nome = forms.CharField(label='Nome', max_length=50, required=False)
    quantidade = forms.IntegerField(label='Quantidade', required=False)

    class Meta:
        model = TipoPosologia
        fields = '__all__'


class TransporteForm(forms.ModelForm):
    class Meta:
        model = Transporte
        fields = '__all__'

class TransporteFilterForm(forms.ModelForm):
    nome_transporte = forms.CharField(label='Nome do transporte', max_length=50, required=False)

    class Meta:
        model = Transporte
        fields = '__all__'


class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ('__all__')


class SalaFilterForm(forms.ModelForm):
    nome_sala = forms.CharField(label='Nome da sala', max_length=50, required=False)

    class Meta:
        model = Sala
        fields = '__all__'

class ProfissionalForm(forms.ModelForm):
    senha = forms.CharField(label='Senha', max_length=1000, required=False)
    confirmacao_senha = forms.CharField(label='Confirmação de Senha', max_length=1000, required=False)
    class Meta:
        model = Profissional
        fields = '__all__'

    def clean_telefone_1(self):
        telefone_1 = self.cleaned_data.get('telefone_1')

        try:
            return telefone_1
        except forms.ValidationError:
            raise forms.ValidationError("Este número de telefone já está associado a uma conta existente.")

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')

        if Usuario.objects.filter(cpf_cnpj=cpf).exists():
            raise forms.ValidationError("Este CPF já está vinculado a uma conta existente.")
        
        return cpf
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            return email
        except forms.ValidationError:
             raise forms.ValidationError("Já existe um usuário registrado com este endereço de e-mail.")

class ProfissionalUpdateViewForm(forms.ModelForm):
    senha = forms.CharField(label='Senha', max_length=1000, required=False)
    confirmacao_senha = forms.CharField(label='Confirmação de Senha', max_length=1000, required=False)

    class Meta:
        model = Profissional
        fields = (
            'nome_profissional', 
            'tipo_profissional', 
            'coren', 
            'crm', 
            'cns', 
            'cbo', 
            'cpf', 
            'endereco', 
            'numero', 
            'complemento', 
            'bairro', 
            'cep', 
            'municipio', 
            'estado', 
            'telefone_1', 
            'telefone_2', 
            'email', 
            'situacao', 
            'senha', 
            'confirmacao_senha', 
            'unidades_saude'
        )

    def clean_telefone_1(self):
        telefone_1 = self.cleaned_data.get('telefone_1')

        try:
            return telefone_1
        except forms.ValidationError:
            raise forms.ValidationError("Este número de telefone já está associado a uma conta existente.")

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')

        if Usuario.objects.filter(cpf_cnpj=cpf).exists():
            raise forms.ValidationError("Este CPF já está vinculado a uma conta existente.")
        
        return cpf
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            return email
        except forms.ValidationError:
             raise forms.ValidationError("Já existe um usuário registrado com este endereço de e-mail.")
    
    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmacao_senha = cleaned_data.get('confirmacao_senha')

        if senha and confirmacao_senha and senha != confirmacao_senha:
            raise forms.ValidationError("Os campos senha e confirmação de senha devem ser iguais.")

        return cleaned_data

class ProfissionalFilterForm(forms.ModelForm):
    nome_profissional = forms.CharField(label='Nome de Profissional', max_length=100, required=False)
    coren = forms.CharField(label='COREN', max_length=7, required=False)
    crm = forms.CharField(label='CRM', max_length=6, required=False)

    class Meta:
        model = Profissional
        fields = ('nome_profissional', 'tipo_profissional', 'coren', 'crm')


class PacienteForm(forms.ModelForm):
    profissao = forms.ModelChoiceField(queryset=Profissao.objects.all(), empty_label="Selecione a Profissão", required=False)
    estado = forms.ModelChoiceField(queryset=Estado.objects.all(), empty_label="Selecione a UF")
   
    class Meta:
        model = Paciente
        fields = '__all__'

class PacienteFilterForm(forms.ModelForm):
    nome_paciente = forms.CharField(label='Nome do Paciente', max_length=200, required=False)

    class Meta:
        model = Paciente
        fields = ('nome_paciente', 'cpf', 'cartao_sus', 'rg')

class SetorForm(forms.ModelForm):
    class Meta:
        model = UnidadeSetor
        fields = ('__all__')

class PainelChamadaForm(forms.ModelForm):
    class Meta:
        model = PainelChamada
        fields = ('nome', 'setores')