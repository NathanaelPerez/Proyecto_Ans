from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    foto_perfil = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'foto_perfil']