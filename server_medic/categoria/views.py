from django.shortcuts import render, get_object_or_404
from .models import Categoria


def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, "categoria/list.html", {"categorias": categorias})


def categoria_detail(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    return render(request, "categoria/detail.html", {"categoria": categoria})
