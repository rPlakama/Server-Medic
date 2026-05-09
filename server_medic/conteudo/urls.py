from django.urls import path
from . import views

app_name = "conteudo"

urlpatterns = [
    path("", views.conteudo_list, name="list"),
    path("criar/", views.conteudo_create, name="create"),
    path("<int:pk>/", views.conteudo_detail, name="detail"),
]