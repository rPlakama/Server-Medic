from django.shortcuts import render, get_object_or_404
from .models import Autor


def autor_list(request):
    autores = Autor.objects.select_related("user")
    return render(request, "autor/list.html", {"autores": autores})


def autor_detail(request, pk):
    autor = get_object_or_404(Autor.objects.select_related("user"), pk=pk)
    return render(request, "autor/detail.html", {"autor": autor})
