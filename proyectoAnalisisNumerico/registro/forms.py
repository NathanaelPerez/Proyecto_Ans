from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from login.models import Perfil

class RegistroForm(UserCreationForm):
    email = forms.EmailField()
    nombres = forms.CharField(label="Nombres", max_length=50)
    apellidos = forms.CharField(label="Apellidos", max_length=50)
    foto_perfil = forms.ImageField(required=False)
    carrera = forms.CharField(max_length=100)
    carnet = forms.CharField(max_length=20)
    ciclo = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
