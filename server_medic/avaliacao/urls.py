from django.urls import path
from . import views

app_name = "avaliacao"

urlpatterns = [
    path("", views.avaliacao_list, name="list"),
    path("<int:pk>/", views.avaliacao_detail, name="detail"),
]