from django.urls import path
from . import views

app_name = "usuario"

urlpatterns = [
    path("", views.usuario_list, name="list"),
    path("criar/", views.usuario_create, name="create"),
    path("<int:pk>/", views.usuario_detail, name="detail"),
]