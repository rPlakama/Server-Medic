import logging
import mimetypes
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.clickjacking import xframe_options_exempt

from server_medic.autor.models import Autor
from server_medic.avaliacao.forms import AvaliacaoForm
from server_medic.avaliacao.models import Avaliacao
from server_medic.comentario.forms import ComentarioForm
from server_medic.comentario.models import Comentario
from server_medic.especialidade.models import Especialidade

from .forms import ConteudoForm
from .models import Conteudo

logger = logging.getLogger(__name__)


def _especialidade_context():
    return {"especialidades": list(Especialidade.objects.order_by("nome"))}


def conteudo_list(request):
    conteudos = Conteudo.objects.select_related("autor", "especialidade", "categoria")
    return render(request, "conteudo/list.html", {"conteudos": conteudos})


def conteudo_detail(request, pk):
    conteudo = get_object_or_404(
        Conteudo.objects.select_related("autor", "especialidade", "categoria"),
        pk=pk,
    )
    comentarios = conteudo.comentarios.select_related("usuario")

    user_rating = None
    rating_form = None
    comment_form = None

    if request.user.is_authenticated:
        user_rating = Avaliacao.objects.filter(
            usuario=request.user, conteudo=conteudo
        ).first()
        rating_form = AvaliacaoForm(instance=user_rating)
        comment_form = ComentarioForm()

    return render(
        request,
        "conteudo/detail.html",
        {
            "conteudo": conteudo,
            "comentarios": comentarios,
            "rating_form": rating_form,
            "user_rating": user_rating,
            "comment_form": comment_form,
        },
    )


@login_required
def conteudo_create(request):
    if request.method == "POST":
        form = ConteudoForm(request.POST, request.FILES)
        if form.is_valid():
            conteudo = form.save(commit=False)
            conteudo.especialidade = form.cleaned_data["especialidade_nome"]
            autor, _ = Autor.objects.get_or_create(
                user=request.user,
                defaults={
                    "nome_plataforma": request.user.username,
                    "crm": request.user.crm,
                    "atuacao": "",
                    "instituicao": "",
                },
            )
            conteudo.autor = autor
            conteudo.save()
            logger.info(
                "Conteudo criado: %s (pk=%s) por %s",
                conteudo.titulo,
                conteudo.pk,
                request.user.email,
            )
            return redirect("conteudo:detail", pk=conteudo.pk)
    else:
        form = ConteudoForm()

    ctx = {"form": form, "action": "Adicionar"}
    ctx.update(_especialidade_context())
    return render(request, "conteudo/form.html", ctx)


@xframe_options_exempt
def conteudo_arquivo_view(request, pk):
    conteudo = get_object_or_404(Conteudo, pk=pk)
    if not conteudo.arquivo:
        from django.http import Http404
        raise Http404("Nenhum arquivo vinculado.")

    content_type, _ = mimetypes.guess_type(conteudo.arquivo.name)
    is_pdf = content_type == "application/pdf"

    response = FileResponse(
        conteudo.arquivo.open("rb"),
        content_type=content_type or "application/octet-stream",
        filename=conteudo.arquivo.name,
    )

    if is_pdf:
        response["Content-Disposition"] = f'inline; filename="{conteudo.arquivo.name}"'

    return response


@login_required
def conteudo_avaliar(request, pk):
    conteudo = get_object_or_404(
        Conteudo.objects.select_related("autor", "especialidade", "categoria"),
        pk=pk,
    )
    avaliacao = Avaliacao.objects.filter(
        usuario=request.user, conteudo=conteudo
    ).first()

    if request.method == "POST":
        form = AvaliacaoForm(request.POST, instance=avaliacao)
        if form.is_valid():
            nova = form.save(commit=False)
            nova.usuario = request.user
            nova.conteudo = conteudo
            nova.save()
            messages.success(request, "Avaliacao salva.")
            return redirect("conteudo:detail", pk=pk)
    else:
        form = None

    comentarios = conteudo.comentarios.select_related("usuario")
    user_rating = avaliacao
    rating_form = form or AvaliacaoForm(instance=avaliacao)
    comment_form = ComentarioForm()

    return render(
        request,
        "conteudo/detail.html",
        {
            "conteudo": conteudo,
            "comentarios": comentarios,
            "rating_form": rating_form,
            "user_rating": user_rating,
            "comment_form": comment_form,
        },
    )


@login_required
def conteudo_comentar(request, pk):
    conteudo = get_object_or_404(
        Conteudo.objects.select_related("autor", "especialidade", "categoria"),
        pk=pk,
    )

    if request.method == "POST":
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.conteudo = conteudo
            comentario.save()
            messages.success(request, "Comentario adicionado.")
            return redirect("conteudo:detail", pk=pk)
    else:
        form = None

    comentarios = conteudo.comentarios.select_related("usuario")
    user_rating = Avaliacao.objects.filter(
        usuario=request.user, conteudo=conteudo
    ).first()
    rating_form = AvaliacaoForm(instance=user_rating)
    comment_form = form or ComentarioForm()

    return render(
        request,
        "conteudo/detail.html",
        {
            "conteudo": conteudo,
            "comentarios": comentarios,
            "rating_form": rating_form,
            "user_rating": user_rating,
            "comment_form": comment_form,
        },
    )
