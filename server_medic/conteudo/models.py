from django.db import models


class Conteudo(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, default="")
    link = models.URLField(max_length=500, blank=True, default="")
    autor = models.ForeignKey(
        "autor.Autor", on_delete=models.CASCADE, related_name="conteudos"
    )
    especialidade = models.ForeignKey(
        "especialidade.Especialidade",
        on_delete=models.CASCADE,
        related_name="conteudos",
    )
    categoria = models.ForeignKey(
        "categoria.Categoria", on_delete=models.CASCADE, related_name="conteudos"
    )
    data_publicacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "conteúdo"
        verbose_name_plural = "conteúdos"
        ordering = ["-data_publicacao"]

    def __str__(self):
        return self.titulo