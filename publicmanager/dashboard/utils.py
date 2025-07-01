from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect

class SaudeCheckHasPermission(object):
    required_permissions = [settings.DESENVOLVEDOR, ]
        
    def has_permissions(self):
        return self.request.user.tipo_usuario in self.required_permissions

    def dispatch(self, request, *args, **kwargs):
        if self.request.user and self.request.user.is_anonymous:
            return redirect('autenticacao:login')
        
        elif not self.has_permissions():
            messages.error(request, "Você não tem permissão para acessar essa página.")
            return redirect('dashboard:index')
        
        elif self.request.user.deve_mudar_senha:
            return redirect('autenticacao:alterar_senha')
        
        return super(SaudeCheckHasPermission, self).dispatch(request, *args, **kwargs)