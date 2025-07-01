from django import forms

from .models import Servidor, PessoaFisica, PessoaJuridica, CargoEmprego, Funcao, JornadaTrabalho, RegimeJuridico, \
    NivelEscolaridade, Situacao


class CargoEmpregoForm(forms.ModelForm):
    class Meta:
        model = CargoEmprego
        fields = '__all__'

class FuncaoForm(forms.ModelForm):
    class Meta:
        model = Funcao
        fields = '__all__'

class JornadaTrabalhoForm(forms.ModelForm):
    class Meta:
        model = JornadaTrabalho
        fields = '__all__'

class RegimeJuridicoForm(forms.ModelForm):
    class Meta:
        model = RegimeJuridico
        fields = '__all__'

class NivelEscolaridadeForm(forms.ModelForm):
    class Meta:
        model = NivelEscolaridade
        fields = '__all__'

class SituacaoForm(forms.ModelForm):
    class Meta:
        model = Situacao
        fields = '__all__'


class PessoaFisicaForm(forms.ModelForm):
    class Meta:
        model = PessoaFisica
        fields =  ('nome_usual', 'nome_social', 'nome_registro', 'email', 'email_secundario',
                   'website', 'cpf', 'sexo', 'grupo_sanguineo','fator_rh', 'titulo_numero',
                   'titulo_zona', 'titulo_secao', 'titulo_uf', 'titulo_data_emissao', 'rg',
                   'rg_orgao', 'rg_data', 'rg_uf', 'nascimento_municipio', 'nascimento_data',
                   'nome_mae', 'nome_pai', 'cnh_registro','cnh_categoria',
                   'cnh_emissao', 'cnh_uf', 'cnh_validade', 'ctps_numero', 'ctps_uf', 'ctps_data_prim_emprego',
                   'ctps_serie', 'pis_pasep', 'pagto_banco', 'pagto_agencia', 'pagto_ccor', 'pagto_ccor_tipo',
                   'estado_civil', 'raca', 'nacionalidade', 'pais_origem', 'deficiencia', 'lattes')


class PessoaJuridicaForm(forms.ModelForm):
    class Meta:
        model = PessoaJuridica
        fields = '__all__'

class ServidorForm(forms.ModelForm):
    pessoa_fisica = forms.ModelChoiceField(queryset=PessoaFisica.objects.all())

    class Meta:
        model = Servidor
        fields = ('pessoa_fisica','setor', 'matricula', 'data_inicio_servico_publico', 'data_inicio_exercicio_na_instituicao',
                  'data_posse_na_instituicao', 'data_posse_no_cargo', 'data_inicio_exercicio_no_cargo',
                  'data_fim_servico_na_instituicao', 'email_institucional', 'cargo_emprego',
                  'cargo_emprego_data_ocupacao',
                  'cargo_emprego_data_saida', 'situacao', 'jornada_trabalho', 'funcao', 'funcao_data_ocupacao',
                  'funcao_data_saida', 'regime_juridico', 'nivel_escolaridade', 'setor_lotacao_data_ocupacao',
                  'setor_exercicio', 'titulo_secao')
