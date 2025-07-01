from .models import *
from django.contrib import admin, messages
from import_export.admin import ImportExportModelAdmin

def reset_password(modeladmin, request, queryset):
    for user in queryset:
        user.update_password(reset=True)
        
    messages.success(request, f'Senhas redefinidas com sucesso para {len(queryset)} usuários.')

reset_password.short_description = '#### Redefinir Senhas ####'

@admin.register(Usuario)
class UsuarioAdmin(ImportExportModelAdmin):
    list_display= ('nome', 'cpf_cnpj', 'email', 'deve_mudar_senha')
    actions = [reset_password]

@admin.register(RegistroAcesso)
class UsuarioAdmin(admin.ModelAdmin):
    list_display= ('usuario', 'endereco_ip', 'caminho', 'data_hora', 'descricao')

@admin.register(PainelUnidadeUsuario)
class PainelUnidadeUsuarioAdmin(admin.ModelAdmin):
    list_display= ('usuario', 'usuario')
