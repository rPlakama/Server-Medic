from django.contrib import admin
from .models import Categoria


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("tipo", "nivel_complexidade")
    list_filter = ("tipo", "nivel_complexidade")