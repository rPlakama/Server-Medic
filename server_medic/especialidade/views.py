from django.shortcuts import render, get_object_or_404
from .models import Especialidade


def especialidade_list(request):
    especialidades = Especialidade.objects.all()
    return render(
        request, "especialidade/list.html", {"especialidades": especialidades}
    )


def especialidade_detail(request, pk):
    especialidade = get_object_or_404(Especialidade, pk=pk)
    return render(
        request, "especialidade/detail.html", {"especialidade": especialidade}
    )
