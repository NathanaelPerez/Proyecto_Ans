# editarperfil/forms.py

from django import forms
from django.contrib.auth.models import User
from login.models import Perfil

class EditarPerfilForm(forms.ModelForm):
    # Campos User
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    nueva_contrasena = forms.CharField(
        label='Nueva contraseña', 
        required=False, 
        widget=forms.PasswordInput,
        help_text='Deja vacío si no quieres cambiar la contraseña'
    )

    # Campos Perfil (definidos en Meta)

    class Meta:
        model = Perfil
        fields = ['nombres', 'apellidos', 'foto_perfil', 'carrera', 'carnet', 'ciclo']

    def __init__(self, *args, **kwargs):
        # Esperamos recibir instancia de Perfil y User para inicializar
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        perfil = super().save(commit=False)
        user = perfil.user

        # Actualizamos user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']

        # Cambiar contraseña si se ingresó nueva
        nueva_contra = self.cleaned_data.get('nueva_contrasena')
        if nueva_contra:
            user.set_password(nueva_contra)

        if commit:
            user.save()
            perfil.save()

        return perfil
