from django.contrib import admin

from publicmanager.saude.models import UnidadeSaude, ResponsavelUnidade, Manual, EsqueceuSenha

@admin.register(UnidadeSaude)
class UnidadeSaudeAdmin(admin.ModelAdmin):
    list_display= ('nome', 'email', 'telefone', 'slug')

@admin.register(ResponsavelUnidade)
class ResponsavelUnidadeAdmin(admin.ModelAdmin):
    list_display= ('unidade_saude', 'profissional')


@admin.register(Manual)
class ManualAdmin(admin.ModelAdmin):
    list_display= ('nome', 'arquivo')

@admin.register(EsqueceuSenha)
class EsqueceuSenhaAdmin(admin.ModelAdmin):
    list_display= ('email', 'whatsapp', 'finalizado')