from django import forms
from .models import SolicitacaoAlvaraFuncionamento


class SolicitacaoAlvaraFuncionamentoForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoAlvaraFuncionamento
        fields = [
            'nome_estabelecimento',
            'cnpj', 
            'endereco',
            'telefone',
            'email',
            'atividade_principal',
            'area_construida',
            'numero_funcionarios',
        ]
        widgets = {
            'nome_estabelecimento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do estabelecimento'
            }),
            'cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00.000.000/0000-00',
                'data-mask': '00.000.000/0000-00'
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o endereço completo'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000',
                'data-mask': '(00) 00000-0000'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o e-mail'
            }),
            'atividade_principal': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descreva a atividade principal do estabelecimento'
            }),
            'area_construida': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'numero_funcionarios': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona classes CSS para todos os campos
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
