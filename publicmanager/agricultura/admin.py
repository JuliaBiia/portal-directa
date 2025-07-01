from django.contrib import admin
from .models import TipoProdutor

@admin.register(TipoProdutor)
class TipoProdutorAdmin(admin.ModelAdmin):
    list_display= ('id', 'descricao')
