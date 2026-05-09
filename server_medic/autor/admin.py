from django.contrib import admin
from .models import Autor


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ("nome_plataforma", "crm", "atuacao", "instituicao")
    search_fields = ("nome_plataforma", "crm")