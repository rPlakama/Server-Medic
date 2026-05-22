from django.shortcuts import render, get_object_or_404
from .models import Comentario


def comentario_list(request):
    comentarios = Comentario.objects.select_related("usuario", "conteudo")
    return render(request, "comentario/list.html", {"comentarios": comentarios})


def comentario_detail(request, pk):
    comentario = get_object_or_404(
        Comentario.objects.select_related("usuario", "conteudo"), pk=pk
    )
    return render(request, "comentario/detail.html", {"comentario": comentario})
