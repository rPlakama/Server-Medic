from django.contrib.auth.models import AbstractUser
from django.db import models


class PerfilChoices(models.TextChoices):
    ESTUDANTE = "estudante", "Estudante"
    PROFISSIONAL = "profissional", "Profissional"


class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField(null=True, blank=True)
    perfil = models.CharField(
        max_length=20,
        choices=PerfilChoices.choices,
        default=PerfilChoices.ESTUDANTE,
    )
    crm = models.CharField(max_length=50, blank=True, default="")
    especialidade_atuacao = models.ForeignKey(
        "especialidade.Especialidade",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profissionais",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "usuário"
        verbose_name_plural = "usuários"

    def __str__(self):
        return self.email


class Progresso(models.Model):
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="progressos"
    )
    conteudo = models.ForeignKey(
        "conteudo.Conteudo", on_delete=models.CASCADE, related_name="progressos"
    )
    concluido = models.BooleanField(default=False)
    data_ultimo_acesso = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "progresso"
        verbose_name_plural = "progressos"
        unique_together = ("usuario", "conteudo")

    def __str__(self):
        return f"{self.usuario.email} - {self.conteudo.titulo}"


class Favorito(models.Model):
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="favoritos"
    )
    conteudo = models.ForeignKey(
        "conteudo.Conteudo", on_delete=models.CASCADE, related_name="favoritos"
    )
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "favorito"
        verbose_name_plural = "favoritos"
        unique_together = ("usuario", "conteudo")

    def __str__(self):
        return f"{self.usuario.email} ★ {self.conteudo.titulo}"