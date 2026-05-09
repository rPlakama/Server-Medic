from django.urls import path
from . import views

app_name = "especialidade"

urlpatterns = [
    path("", views.especialidade_list, name="list"),
    path("<int:pk>/", views.especialidade_detail, name="detail"),
]