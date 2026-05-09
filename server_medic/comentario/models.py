from django.db import models
from django.conf import settings


class Comentario(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comentarios"
    )
    conteudo = models.ForeignKey(
        "conteudo.Conteudo", on_delete=models.CASCADE, related_name="comentarios"
    )
    texto = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "comentário"
        verbose_name_plural = "comentários"
        ordering = ["-data"]

    def __str__(self):
        return f"{self.usuario.email} em {self.conteudo.titulo}"