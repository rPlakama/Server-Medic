from django.contrib import admin
from .models import Usuario, Progresso, Favorito


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "perfil", "especialidade_atuacao", "data_nascimento", "is_active")
    list_filter = ("perfil", "is_active")
    search_fields = ("email", "username", "crm")


@admin.register(Progresso)
class ProgressoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "conteudo", "concluido", "data_ultimo_acesso")
    list_filter = ("concluido",)


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "conteudo", "data")