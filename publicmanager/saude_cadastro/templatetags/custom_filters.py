import unicodedata
from django import template
from publicmanager.saude_cadastro.models import Sala, UnidadeSetor

from publicmanager.saude_farmacia.models import Farmacia, Medicamento, Produto, RequisicaoMaterialFarmacia
from publicmanager.saude_atendimento.models import Paciente

register = template.Library()

@register.filter
def list_element_by_index(lista, indice):
    try:
        print(lista[indice])
        return lista[indice]
    except (IndexError, TypeError):
        return None

@register.filter
def enumerate_queryset(queryset):
    try:
        return list(enumerate(queryset))
    except (IndexError, TypeError):
        return None

@register.filter
def convert_number_day_for_string_day(number_day):
        DOMINGO = 0
        SEGUNDA = 1
        TERCA = 2
        QUARTA = 3
        QUINTA = 4
        SEXTA = 5
        SABADO = 6
        DIA_SEMANA_CHOICES = [
            (DOMINGO, 'Domingo'),
            (SEGUNDA, 'Segunda'),
            (TERCA, 'Terça'),
            (QUARTA, 'Quarta'),
            (QUINTA, 'Quinta'),
            (SEXTA, 'Sexta'),
            (SABADO, 'Sábado'),
        ]

        try:
             return DIA_SEMANA_CHOICES[number_day][1]
        except (IndexError, TypeError):
             return None

@register.filter
def join_to_error_messages(form):
    erros = []
    array_mensagens_de_erro = []

    for field in form:
        for error in field.errors:
            erros.append(error)
            array_mensagens_de_erro.append({"field_label": field.label, "error": error})

    for field_errors in form.errors.values():
        for error in field_errors:
            if not(error in erros):
                erros.append(error)
                array_mensagens_de_erro.append({"field_label": "", "error": error})

    return array_mensagens_de_erro

@register.filter
def get_element_dict(dictionary, key):
    return dictionary[key]

@register.filter
def return_situacao_choice_option_text(choice_option_int):
    return Farmacia.SITUACAO_CHOICES[choice_option_int][1]

@register.filter
def return_situacao_requisicao_choice_option_text(choice_option_int):
    return RequisicaoMaterialFarmacia.TIPO_SITUACAO_CHOICES[choice_option_int][1]

@register.filter
def return_situacao_unidade_setor_choice_option_text(choice_option_int):
    return UnidadeSetor.SITUACAO_CHOICES[choice_option_int][1]

@register.filter
def return_situacao_sala_choice_option_text(choice_option_int):
    return Sala.SITUACAO_CHOICES[choice_option_int][1]

@register.filter
def return_tipo_farmacia_choice_option_text(choice_option_int):
    return Farmacia.TIPO_FARMACIA_CHOICES[choice_option_int][1]

@register.filter
def return_tipo_produto_choice_option_text(choice_option_int):
    return Produto.TIPO_PRODUTO_CHOICES[choice_option_int][1]

@register.filter
def return_tipo_medicamento_choice_option_text(choice_option_int):
    return Medicamento.TIPO_MEDICAMENTO_CHOICES[choice_option_int][1]

@register.filter
def return_raca_choice_option_text(choice_option_int):
    return Paciente.RACA_CHOICES[choice_option_int][1]

@register.filter
def return_positive_or_negative_value_fator_rh(fator_rh):
    if fator_rh == "+":
        return 'POSITIVO'
    elif fator_rh == '-':
        return 'NEGATIVO'

@register.filter
def plus_one(value):
    return int(value)+1

@register.filter
def startswith(string, substring):
    return string.startswith(substring)

@register.filter
def remover_acentos(value):
    if value is not None:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('utf-8')
        value = value.lower()
    return value

@register.filter
def format_duration(value):

    value = str(value).split(":")

    if int(value[0]) < 10:
        value[0] = "0"+value[0]

    return ":".join(value)