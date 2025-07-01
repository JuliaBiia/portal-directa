from django.utils.timezone import now
from publicmanager.autenticacao.models import RegistroAcesso

def registrar_acesso(requisicao, usuario, sucesso, descricao, erros=None):
    endereco_ip = obter_endereco_ip(requisicao)
    caminho = requisicao.path
    registro = RegistroAcesso(usuario=usuario, endereco_ip=endereco_ip, caminho=caminho, data_hora=now(), descricao=descricao)
    registro.save()

    if not sucesso:
        print(f"Falha no login: {erros}")

def obter_endereco_ip(requisicao):
    x_forwarded_for = requisicao.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return requisicao.META.get('REMOTE_ADDR')