import unicodedata
from django import template
from django.utils import timezone

from publicmanager.saude_enfermagem.models import ListaChamadaSolicitacaoAtendimento, SituacaoMedicacaoAtendimento, ListaChamadoAdministracaoMedicamento

register = template.Library()

@register.filter
def get_data_hora_atendimento(lista):
    query = lista.filter(situacao=ListaChamadaSolicitacaoAtendimento.DESIGNADO).first()
    return timezone.localtime(query.created_at).strftime("%d/%m/%Y")

@register.filter
def get_hora_atendimento(lista):
    query = lista.filter(situacao=ListaChamadaSolicitacaoAtendimento.DESIGNADO).first()
    return timezone.localtime(query.created_at).strftime("%H:%m")

@register.filter
def verificar_temperatura(lista, profissional_id):
    return lista.filter(profissional__id=profissional_id).first().temperatura

@register.filter
def verificar_tipo_classificacao_risco(lista, profissional_id):
    return lista.filter(profissional__id=profissional_id).first().tipo_classificacao_risco.tipo

@register.filter
def verificar_presao_arterial(lista, profissional_id):
    return lista.filter(profissional__id=profissional_id).first().presao_arterial

@register.filter
def verificar_medicacao_atendimento(lista, profissional_id):
    for medicacao in lista:
        if SituacaoMedicacaoAtendimento.objects.filter(enfermeiro__id=profissional_id, medicacao_atendimento=medicacao).exists():
            return True
    return False

@register.filter
def get_data_hora_atendimento_medicacao(lista):
    query = lista.filter(situacao=ListaChamadoAdministracaoMedicamento.DESIGNADO).first()
    if query:
        return timezone.localtime(query.created_at).strftime("%d/%m/%Y - %H:%m")
    else:
        return '-----'