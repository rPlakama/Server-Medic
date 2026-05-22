from django import forms
from django.core.exceptions import ValidationError
from server_medic.especialidade.models import Especialidade
from .models import Conteudo


class ConteudoForm(forms.ModelForm):
    especialidade_nome = forms.CharField(
        required=True,
        label="Especialidade",
        widget=forms.TextInput(attrs={
            "list": "especialidade-list",
            "autocomplete": "off",
            "placeholder": "Digite para buscar...",
        }),
    )

    class Meta:
        model = Conteudo
        fields = [
            "titulo",
            "descricao",
            "link",
            "corpo",
            "arquivo",
            "categoria",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.especialidade_id:
            self.fields["especialidade_nome"].initial = self.instance.especialidade.nome

    def clean_especialidade_nome(self):
        nome = self.cleaned_data["especialidade_nome"].strip()
        if not nome:
            raise ValidationError("Selecione uma especialidade.")
        especialidade = Especialidade.objects.filter(nome__iexact=nome).first()
        if not especialidade:
            raise ValidationError(f'Especialidade "{nome}" nao encontrada. Escolha uma da lista.')
        return especialidade
