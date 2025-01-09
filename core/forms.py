from django import forms

from core.models import Ativo


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Nome do usuário')
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')

class CreateAtivo(forms.ModelForm):
    class Meta:
        model = Ativo
        fields = ['ticker', 'limite_inferior', 'limite_superior', 'periodicidade']