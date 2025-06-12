from django.shortcuts import render, redirect
from .forms import RegistroForm
from django.contrib.auth import login
from login.models import Perfil

# Create your views here.
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save()
            foto = form.cleaned_data.get('foto_perfil')
            Perfil.objects.create(user=usuario, foto_perfil=foto)
            login(request, usuario)
            return redirect('home')
    else:
        form = RegistroForm()
    
    return render(request, 'registro.html', {'form': form})
