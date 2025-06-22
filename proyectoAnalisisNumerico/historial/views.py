from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import HistorialCalculo

@login_required
def historial_view(request):
    historial = HistorialCalculo.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'historial/historial.html', {'historial': historial})
