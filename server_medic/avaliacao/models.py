from django.db import models
from django.conf import settings


class Avaliacao(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="avaliacoes"
    )
    conteudo = models.ForeignKey(
        "conteudo.Conteudo", on_delete=models.CASCADE, related_name="avaliacoes"
    )
    nota = models.PositiveSmallIntegerField()
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "avaliação"
        verbose_name_plural = "avaliações"
        unique_together = ("usuario", "conteudo")

    def __str__(self):
        return f"{self.usuario.email} - {self.conteudo.titulo} ({self.nota})"