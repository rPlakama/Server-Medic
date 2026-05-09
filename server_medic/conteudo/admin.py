from django.contrib import admin
from .models import Conteudo


@admin.register(Conteudo)
class ConteudoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "especialidade", "categoria", "data_publicacao")
    list_filter = ("especialidade", "categoria", "data_publicacao")
    search_fields = ("titulo", "descricao")