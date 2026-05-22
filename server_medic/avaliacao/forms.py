from django import forms
from .models import Avaliacao


class AvaliacaoForm(forms.ModelForm):
    nota = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.Select,
        label="Nota",
    )

    class Meta:
        model = Avaliacao
        fields = ["nota"]
