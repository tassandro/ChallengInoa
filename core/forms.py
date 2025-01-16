from django import forms
from core.models import Ativo

class CreateAtivo(forms.ModelForm):
    # ticker = forms.ModelChoiceField(queryset=Ticker.objects.order_by('codigo'), empty_label="Selecione um ticker")

    class Meta:
        model = Ativo
        fields = ['ticker', 'limite_inferior', 'limite_superior', 'periodicidade']