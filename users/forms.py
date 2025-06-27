from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=("Senha"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label=("Confirmação de senha"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ('email', 'nome_completo', 'endereco', 'telefone')
        labels = {
            'email': _('Email'),
            'nome_completo': ('Nome Completo'),
            'endereco': ('Endereço'),
            'telefone': ('Telefone'),
        }
        widgets = {
            'endereco': forms.Textarea(attrs={'rows': 3}),
        }
