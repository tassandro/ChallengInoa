from django import forms
from core.models import Ativo

class CreateAtivo(forms.ModelForm):
    class Meta:
        model = Ativo
        fields = ['ticker', 'limite_inferior', 'limite_superior', 'periodicidade']

    
