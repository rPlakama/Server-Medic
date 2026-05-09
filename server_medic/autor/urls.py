from django.urls import path
from . import views

app_name = "autor"

urlpatterns = [
    path("", views.autor_list, name="list"),
    path("<int:pk>/", views.autor_detail, name="detail"),
]