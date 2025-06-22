from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EditarPerfilForm

@login_required
def editar_perfil(request):
    perfil = request.user.perfil

    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, request.FILES, instance=perfil, user=request.user)
        if form.is_valid():
            form.save()
            # Ojo: Si cambiaste contraseña, considera hacer login() otra vez
            return redirect('home')
    else:
        form = EditarPerfilForm(instance=perfil, user=request.user)

    return render(request, 'editar_perfil.html', {'form': form, 'perfil': perfil})
