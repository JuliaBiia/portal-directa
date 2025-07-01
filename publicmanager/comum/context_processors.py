
from django.conf import settings

def global_settings(request):
    return {
        'DEBUG': settings.DEBUG,
        'BASE_URL': settings.BASE_URL,
        'SITE_URL': settings.SITE_URL,
        'ADMIN_URL': settings.ADMIN_URL,
        'DEVELOPMENT': settings.DEVELOPMENT,
        'user_name': request.user if request.user else "Sem Usuário"
    }  