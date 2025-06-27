from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import User  # ou from products.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nome_completo = forms.CharField(max_length=150, required=True)
    endereco = forms.CharField(widget=forms.Textarea, required=False)
    telefone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ('email', 'nome_completo', 'endereco', 'telefone', 'password1', 'password2')
        labels = {
            'email': _('Email'),
            'nome_completo': _('Nome Completo'),
            'endereco': _('Endereço'),
            'telefone': _('Telefone'),
        }