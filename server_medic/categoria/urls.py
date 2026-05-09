from django.urls import path
from . import views

app_name = "categoria"

urlpatterns = [
    path("", views.categoria_list, name="list"),
    path("<int:pk>/", views.categoria_detail, name="detail"),
]