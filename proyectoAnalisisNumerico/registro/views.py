from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroForm
from login.models import Perfil

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save()
            
            nombres = form.cleaned_data.get('nombres')
            apellidos = form.cleaned_data.get('apellidos')
            foto = form.cleaned_data.get('foto_perfil')
            carrera = form.cleaned_data.get('carrera')
            carnet = form.cleaned_data.get('carnet')
            ciclo = form.cleaned_data.get('ciclo')

            Perfil.objects.create(
                user=usuario,
                nombres=nombres,
                apellidos=apellidos,
                foto_perfil=foto,
                carrera=carrera,
                carnet=carnet,
                ciclo=ciclo
            )

            login(request, usuario)
            return redirect('home')
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})
