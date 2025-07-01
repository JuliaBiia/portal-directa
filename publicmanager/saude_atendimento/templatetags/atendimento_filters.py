from django import template

from publicmanager.saude.models import UnidadeLogin
from publicmanager.saude_atendimento.models import ClassificacaoRisco, ListaChamada

register = template.Library()

@register.filter
def get_filtrar_setor_tipo(salas, tipo):
    return salas.filter(unidade_setor__tipo=tipo)

@register.filter
def get_contar_salas_tipo(salas, tipo):
    return salas.filter(unidade_setor__tipo=tipo).count()

@register.filter
def get_usuarios_sala(sala):
    return UnidadeLogin.objects.filter(sala=sala).count()

@register.filter
def verificar_profissional_sala(unidades_login, pk):
    if unidades_login.filter(sala__pk=pk).exists():
        return unidades_login.get(sala__pk=pk).profissional.nome_profissional
    return ''

@register.filter
def verificar_ocupacao_sala(unidades_login, pk):
    return unidades_login.filter(sala__pk=pk).exists() if True else False

@register.filter
def filtrar_classificacao_display_ativa(query):
    classificacao_risco = query.filter(status=ClassificacaoRisco.ATIVO).first()

    if classificacao_risco:
        return classificacao_risco.tipo_classificacao_risco.get_cor_display()
    return ''

@register.filter
def filtrar_classificacao_ativa_id(query):
    classificacao_risco = query.filter(status=ClassificacaoRisco.ATIVO).first()

    if classificacao_risco:
        return classificacao_risco.id
    return None

@register.filter
def verificar_classificacao_editar(query):
    lista_chamada = ListaChamada.objects.filter(classificacao_risco__in=query.values('id')).exclude(situacao__in=[ListaChamada.EM_ESPERA, ListaChamada.EM_ATENDIMENTO]).exists()
    if not lista_chamada:
        return True
    return False