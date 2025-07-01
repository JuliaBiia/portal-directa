from django.contrib import admin
# Register your models here.

from publicmanager.rh.models import (
    PessoaFisica, PessoaJuridica, CargoEmprego,
    Situacao, JornadaTrabalho, Funcao, RegimeJuridico,
    NivelEscolaridade, Servidor
)

@admin.register(PessoaFisica)
class PessoaFisicaAdmin(admin.ModelAdmin):
    list_display= ('user', 'nome_usual')

@admin.register(PessoaJuridica)
class PessoaJuridicaAdmin(admin.ModelAdmin):
    list_display= ('razao_social', 'nome_fantasia', 'cnpj')

@admin.register(CargoEmprego)
class CargoEmpregoAdmin(admin.ModelAdmin):
    list_display= ('codigo', 'nome_amigavel', 'descricao')

@admin.register(Situacao)
class SituacaoAdmin(admin.ModelAdmin):
    list_display= ('codigo', 'descricao')

@admin.register(JornadaTrabalho)
class JornadaTrabalhoAdmin(admin.ModelAdmin):
    list_display= ('codigo', 'descricao')

@admin.register(Funcao)
class FuncaoAdmin(admin.ModelAdmin):
    list_display= ('codigo', 'descricao')

@admin.register(RegimeJuridico)
class RegimeJuridicoAdmin(admin.ModelAdmin):
    list_display= ('id', 'codigo_regime', 'sigla')

@admin.register(NivelEscolaridade)
class NivelEscolaridadeAdmin(admin.ModelAdmin):
    list_display= ('codigo', 'descricao')

@admin.register(Servidor)
class ServidorAdmin(admin.ModelAdmin):
    list_display= ('pessoa_fisica', 'setor')
