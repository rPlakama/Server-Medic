from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from server_medic.especialidade.models import Especialidade
from .models import Usuario


class UsuarioRegistrationForm(UserCreationForm):
    especialidade_atuacao_nome = forms.CharField(
        required=False,
        label="Especialidade de atuacao",
        widget=forms.TextInput(attrs={
            "list": "especialidade-list",
            "autocomplete": "off",
            "placeholder": "Digite para buscar...",
        }),
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = [
            "email",
            "username",
            "data_nascimento",
            "perfil",
            "crm",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["crm"].required = False
        if self.instance and self.instance.pk and self.instance.especialidade_atuacao_id:
            self.fields["especialidade_atuacao_nome"].initial = (
                self.instance.especialidade_atuacao.nome
            )

    def clean_especialidade_atuacao_nome(self):
        nome = self.cleaned_data["especialidade_atuacao_nome"].strip()
        if not nome:
            return None
        especialidade = Especialidade.objects.filter(nome__iexact=nome).first()
        if not especialidade:
            raise ValidationError(f'Especialidade "{nome}" nao encontrada. Escolha uma da lista.')
        return especialidade
