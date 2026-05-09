from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("usuario/", include("server_medic.usuario.urls")),
    path("conteudo/", include("server_medic.conteudo.urls")),
    path("especialidade/", include("server_medic.especialidade.urls")),
    path("autor/", include("server_medic.autor.urls")),
    path("avaliacao/", include("server_medic.avaliacao.urls")),
    path("comentario/", include("server_medic.comentario.urls")),
    path("categoria/", include("server_medic.categoria.urls")),
]