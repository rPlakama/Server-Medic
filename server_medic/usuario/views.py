from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from server_medic.especialidade.models import Especialidade

from .forms import UsuarioRegistrationForm
from .models import Usuario


def usuario_create(request):
    if request.method == "POST":
        form = UsuarioRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            especialidade = form.cleaned_data.get("especialidade_atuacao_nome")
            if especialidade:
                user.especialidade_atuacao = especialidade
            user.save()
            login(request, user)
            return redirect("conteudo:list")
    else:
        form = UsuarioRegistrationForm()
    ctx = {"form": form}
    ctx["especialidades"] = list(Especialidade.objects.order_by("nome"))
    return render(request, "usuario/registro.html", ctx)


@login_required
def usuario_list(request):
    usuarios = Usuario.objects.all()
    return render(request, "usuario/list.html", {"usuarios": usuarios})


@login_required
def usuario_detail(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    return render(request, "usuario/detail.html", {"usuario_obj": usuario})
