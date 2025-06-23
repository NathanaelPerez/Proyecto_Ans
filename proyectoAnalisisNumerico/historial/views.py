from django.shortcuts import render, redirect
from .models import HistorialCalculo
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localtime
from datetime import timedelta

@login_required
def historial_list(request):
    historial = HistorialCalculo.objects.filter(usuario=request.user).order_by('-fecha')
    # Convertimos a UTC-6 manualmente
    for h in historial:
        h.fecha_utc6 = localtime(h.fecha) - timedelta(hours=6)
    return render(request, 'historial.html', {'historial': historial})
