import re
from django import template
from datetime import timedelta
from urllib.parse import urlparse
from django.utils import timezone

register = template.Library()

@register.filter
def tempo_medio_espera_data_hora(tempo):
    tempo_atendimento = timezone.timedelta()
    hora_atual = timezone.now()
    tempo_espera = hora_atual - tempo

    dias = tempo_espera.days
    horas, segundos_restantes = divmod(tempo_espera.seconds, 3600)
    minutos, segundos = divmod(segundos_restantes, 60)

    if dias > 0:
        horas += dias * 24

    tempo_espera_formatado = timedelta(hours=horas, minutes=minutos, seconds=segundos)

    tempo_espera_final = max(tempo_espera_formatado, tempo_atendimento)

    if tempo_espera_final.days == 0:
        return f"{tempo_espera_final.seconds // 3600}:{(tempo_espera_final.seconds % 3600) // 60}:{tempo_espera_final.seconds % 60}"
    elif tempo_espera_final.days == 1:
        return f"{tempo_espera_final.days} dia, {tempo_espera_final.seconds // 3600}:{(tempo_espera_final.seconds % 3600) // 60}:{tempo_espera_final.seconds % 60}"
    else:
        return f"{tempo_espera_final.days} dias, {tempo_espera_final.seconds // 3600}:{(tempo_espera_final.seconds % 3600) // 60}:{tempo_espera_final.seconds % 60}"
    
@register.filter
def tempo_medio_espera_hora(tempo):
    hora_atual = timezone.now()
    tempo_espera = hora_atual - tempo
    horas, minutos, segundos = tempo_espera.days * 24 + tempo_espera.seconds // 3600, (tempo_espera.seconds % 3600) // 60, tempo_espera.seconds % 60

    tempo_formatado = "{:02d}:{:02d}:{:02d}".format(horas, minutos, segundos)

    return str(tempo_formatado)

@register.filter
def format_cpf(value):
    if value and len(value) == 11 and value.isdigit():
        return f"{value[:3]}.{value[3:6]}.{value[6:9]}-{value[9:]}"
    return value

@register.filter
def verificacao_tempo_limite(tempo, limite):
    created_at = tempo

    if timezone.is_naive(created_at):
        created_at = timezone.make_aware(created_at)

    if limite is None:
        return False

    if not isinstance(limite, timedelta):
        raise ValueError("limite deve ser um objeto timedelta")

    deadline = created_at + limite

    current_time = timezone.now()

    return current_time > deadline

@register.filter
def comparar_urls(url1, url2):
    # Função para remover a parte da PK do caminho da URL
    def remover_pk(url):
        parts = url.split('/')
        parts = [part for part in parts if not re.match(r'[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}', part)]
        return '/'.join(parts)

    caminho_url1 = urlparse(url1).path
    caminho_url2 = urlparse(url2).path

    caminho_sem_pk1 = remover_pk(caminho_url1)
    caminho_sem_pk2 = remover_pk(caminho_url2)

    return caminho_sem_pk1 == caminho_sem_pk2