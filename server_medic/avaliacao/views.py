from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Avaliacao


@login_required
def avaliacao_list(request):
    avaliacoes = Avaliacao.objects.select_related("usuario", "conteudo")
    return render(request, "avaliacao/list.html", {"avaliacoes": avaliacoes})


@login_required
def avaliacao_detail(request, pk):
    from django.shortcuts import get_object_or_404
    avaliacao = get_object_or_404(
        Avaliacao.objects.select_related("usuario", "conteudo"), pk=pk
    )
    return render(request, "avaliacao/detail.html", {"avaliacao": avaliacao})
