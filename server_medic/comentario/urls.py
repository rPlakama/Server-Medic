from django.urls import path
from . import views

app_name = "comentario"

urlpatterns = [
    path("", views.comentario_list, name="list"),
    path("<int:pk>/", views.comentario_detail, name="detail"),
]