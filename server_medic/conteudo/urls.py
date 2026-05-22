from django.urls import path
from . import views

app_name = "conteudo"

urlpatterns = [
    path("", views.conteudo_list, name="list"),
    path("criar/", views.conteudo_create, name="create"),
    path("<int:pk>/", views.conteudo_detail, name="detail"),
    path("<int:pk>/avaliar/", views.conteudo_avaliar, name="avaliar"),
    path("<int:pk>/comentar/", views.conteudo_comentar, name="comentar"),
    path("<int:pk>/arquivo/", views.conteudo_arquivo_view, name="arquivo"),
]