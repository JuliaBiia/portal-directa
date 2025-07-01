from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import (
    Municipio, GrupoDeficiencia, Raca,
    Deficiencia, EstadoCivil, Banco, Pais, Estado
)
@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display= ('estado', 'sigla')

class MunicipioResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        if 'id' in row:
            del row['id']

    class Meta:
        model = Municipio

@admin.register(Municipio)
class MunicipioAdmin(ImportExportModelAdmin):
    resource_classes = [MunicipioResource]
    list_display= ('nome', 'ibge')

@admin.register(GrupoDeficiencia)
class GrupoDeficienciaAdmin(admin.ModelAdmin):
    list_display= ('id', 'codigo')

@admin.register(Deficiencia)
class DeficienciaAdmin(admin.ModelAdmin):
    list_display= ('id', 'codigo', 'grupo_deficiencia')

@admin.register(EstadoCivil)
class EstadoCivilAdmin(admin.ModelAdmin):
    list_display= ('id', 'nome')

@admin.register(Banco)
class BancoAdmin(admin.ModelAdmin):
    list_display= ('codigo', 'ispb', 'nome_curto')

@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display= ('codigo', 'nome')

@admin.register(Raca)
class RacaAdmin(admin.ModelAdmin):
    list_display= ('id', 'descricao')