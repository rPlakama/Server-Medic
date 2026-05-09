from django.db import models


class TipoChoices(models.TextChoices):
    ARTIGO = "artigo", "Artigo"
    VIDEO = "video", "Vídeo"
    CASO_CLINICO = "caso_clinico", "Caso Clínico"


class NivelChoices(models.TextChoices):
    BASICO = "basico", "Básico"
    INTERMEDIARIO = "intermediario", "Intermediário"
    AVANCADO = "avancado", "Avançado"


class Categoria(models.Model):
    tipo = models.CharField(max_length=20, choices=TipoChoices.choices)
    nivel_complexidade = models.CharField(
        max_length=20, choices=NivelChoices.choices, default=NivelChoices.BASICO
    )

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.get_nivel_complexidade_display()}"