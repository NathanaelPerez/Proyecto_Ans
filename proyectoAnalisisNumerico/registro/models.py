from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.
class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    foto = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']