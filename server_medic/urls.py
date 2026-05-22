from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/conteudo/"), name="logout"),
    path("usuario/", include("server_medic.usuario.urls")),
    path("conteudo/", include("server_medic.conteudo.urls")),
    path("especialidade/", include("server_medic.especialidade.urls")),
    path("autor/", include("server_medic.autor.urls")),
    path("avaliacao/", include("server_medic.avaliacao.urls")),
    path("comentario/", include("server_medic.comentario.urls")),
    path("categoria/", include("server_medic.categoria.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)