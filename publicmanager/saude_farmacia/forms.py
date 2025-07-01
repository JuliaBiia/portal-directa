from datetime import datetime
from django import forms

from publicmanager.saude_farmacia.models import (
    EntradaMaterialFarmacia, InsumoEntrada, Medicamento, Farmacia, InsumoRequisitado, Insumo, MedicamentoEntrada,
    MedicamentoRequisitado, Produto, ProdutoEntrada, ProdutoRequisitado, RequisicaoMaterialFarmacia, PrincipioAtivo
)

class FarmaciaForm(forms.ModelForm):
    class Meta:
        model = Farmacia
        fields = '__all__'


class ProdutoForm(forms.ModelForm):

    class Meta:
        model = Produto
        fields = '__all__'


class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = '__all__'

class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = '__all__'


class InsumoRequisitadoForm(forms.ModelForm):
    class Meta:
        model = InsumoRequisitado
        fields = '__all__'

class MedicamentoRequisitadoForm(forms.ModelForm):
    class Meta:
        model = MedicamentoRequisitado
        fields = '__all__'

class ProdutoRequisitadoForm(forms.ModelForm):
    class Meta:
        model = ProdutoRequisitado
        fields = '__all__'


class InsumoEntradaForm(forms.ModelForm):
    class Meta:
        model = InsumoEntrada
        fields = '__all__'
class MedicamentoEntradaForm(forms.ModelForm):
    class Meta:
        model = MedicamentoEntrada
        fields = '__all__'

class ProdutoEntradaForm(forms.ModelForm):
    class Meta:
        model = ProdutoEntrada
        fields = '__all__'


class RequisicaoMaterialFarmaciaForm(forms.ModelForm):
    class Meta:
        model = RequisicaoMaterialFarmacia
        exclude = ('farmaceutico_solicitante',)


class EntradaMaterialFarmaciaForm(forms.ModelForm):
    class Meta:
        model = EntradaMaterialFarmacia
        exclude = ('farmaceutico_responsavel',)
    
    def clean(self):
        cleaned_data = super().clean()

        data_entrada = cleaned_data.get('data_entrada')

        if data_entrada and data_entrada > datetime.now().date():
            raise forms.ValidationError("A data de entrada deve ser igual ou anterior a data atual.")

        return cleaned_data



class PrincipioAtivoForm(forms.ModelForm):
    class Meta:
        model = PrincipioAtivo
        fields = '__all__'

class PrincipioAtivoFilterForm(forms.ModelForm):
    nome = forms.CharField(label='Nome', max_length=55, required=False)

    class Meta:
        model = PrincipioAtivo
        fields = '__all__'