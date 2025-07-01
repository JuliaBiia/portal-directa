import csv
import uuid
from datetime import datetime
from django.contrib import admin
from django.http import HttpResponse
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from publicmanager.saude.models import UnidadeLogin
from publicmanager.saude_cadastro.models import (
    TipoClinica, Convenio, CID, DestinoObito, TipoExame, Exame, TipoHistoriaClinica,
    TipoPosologia, Transporte, Sala, Profissional, Profissao, PainelChamada,
    Procedimento, UnidadeSetor, TipoClassificacaoRisco
)

def export_profissionais(self, request, queryset):
    unique = uuid.uuid4()
    file_name = f'{datetime.now().strftime("%Y-%m-%d")}-{unique}-profissionais.csv'

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    writer = csv.writer(response)

    writer.writerow(
        ["Nome", 
        "Unidade de Saúde", 
        "Unidade de Saúde ID", 
        "Tipo Profissional",
        "Senha",
        "Coren", 
        "CRM", 
        "CNS", 
        "CBO",
        "CPF",
        "Endereco",
        "Numero",
        "Complemento",
        "Bairro",
        "CEP",
        "Estado",
        "Municipio",
        "Telefone 1",
        "Telefone 2",
        "E-mail",
        "Situacao",
    ])
    for profissional in queryset:

        content = [
            profissional.nome_profissional, 
            ', '.join([unidade.nome for unidade in profissional.unidades_saude.all()]), 
            ', '.join([str(unidade.id) for unidade in profissional.unidades_saude.all()]), 
            profissional.tipo_profissional,
            profissional.user.password,
            profissional.coren, 
            profissional.crm, 
            profissional.cns,
            profissional.cbo,
            profissional.cpf,
            profissional.endereco,
            profissional.numero,
            profissional.complemento,
            profissional.bairro,
            profissional.cep,
            profissional.estado.estado,
            profissional.municipio.nome,
            profissional.telefone_1,
            profissional.telefone_2,
            profissional.email,
            profissional.situacao,
        ]
        writer.writerow(content)
    return response

export_profissionais.short_description = "EXPORTAÇÃO DE PROFISSIONAIS CSV"

@admin.register(TipoClinica)
class TipoClinicaAdmin(admin.ModelAdmin):
    list_display= ('id', 'descricao')

@admin.register(Convenio)
class ConvenioAdmin(admin.ModelAdmin):
    list_display= ('id', 'nome')

@admin.register(CID)
class CIDAdmin(admin.ModelAdmin):
    list_display= ('codigo', 'nome')
    search_fields = ('codigo', 'nome')

@admin.register(DestinoObito)
class DestinoObitoAdmin(admin.ModelAdmin):
    list_display= ('id', 'situacao', 'nome_destino_obito')

@admin.register(TipoExame)
class TipoExameAdmin(admin.ModelAdmin):
    list_display= ('id', 'nome', 'tipo')

@admin.register(Exame)
class ExameAdmin(admin.ModelAdmin):
    list_display= ('id', 'nome', 'tipo_exame')

@admin.register(TipoHistoriaClinica)
class TipoHistoriaClinicaAdmin(admin.ModelAdmin):
    list_display= ('situacao', 'nome')

@admin.register(TipoPosologia)
class TipoDePosologiaAdmin(admin.ModelAdmin):
    list_display= ('nome', 'quantidade', 'antes_da_refeicao', 'pos_refeicao')

@admin.register(Transporte)
class TransporteAdmin(admin.ModelAdmin):
    list_display= ('id', 'situacao', 'nome_transporte')

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display= ('nome_sala', 'unidade_setor')

@admin.register(Procedimento)
class ProcedimentoAdmin(admin.ModelAdmin):
    list_display= ('nome', 'codigo')
    search_fields = ('codigo', 'nome')

class ProfissaoResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        if 'id' in row:
            del row['id']

    class Meta:
        model = Profissao

@admin.register(Profissao)
class ProfissaoAdmin(ImportExportModelAdmin):
    resource_classes = [ProfissaoResource]
    list_display= ('codigo', 'titulo')

@admin.register(PainelChamada)
class PainelChamadaAdmin(admin.ModelAdmin):
    list_display= ('nome', 'unidade_saude', 'slug')

@admin.register(UnidadeSetor)
class UnidadeSetorAdmin(admin.ModelAdmin):
    list_display= ('nome', 'unidade_saude')

class UnidadeLoginInline(admin.TabularInline):
    model = UnidadeLogin
    extra = 0
    show_change_link = True
    readonly_fields = ['unidade',]

@admin.register(Profissional)
class ProfissionalAdmin(ImportExportModelAdmin):
    list_display= ('nome_profissional', 'tipo_profissional')
    actions = [export_profissionais,]
    inlines = [UnidadeLoginInline,]
    
@admin.register(TipoClassificacaoRisco)
class TipoClassificacaoRiscoAdmin(admin.ModelAdmin):
    list_display= ('ordem', 'tipo', 'tempo_atendimento', 'situacao', 'cor', 'unidade_saude')
