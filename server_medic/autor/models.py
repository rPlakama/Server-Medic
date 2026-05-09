from django.db import models
from django.conf import settings


class Autor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="autor"
    )
    nome_plataforma = models.CharField(max_length=150)
    crm = models.CharField(max_length=50)
    atuacao = models.CharField(max_length=200)
    instituicao = models.CharField(max_length=200)

    class Meta:
        verbose_name = "autor"
        verbose_name_plural = "autores"

    def __str__(self):
        return self.nome_plataforma