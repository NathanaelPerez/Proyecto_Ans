from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import RichardsonForm
from .richardson import richardson_derivative

def index(request):
    tabla = []
    pasos = []
    error = None
    resultado_final = None

    if request.method == 'POST':
        form = RichardsonForm(request.POST)
        if form.is_valid():
            funcion = form.cleaned_data['function']
            x = form.cleaned_data['x']
            h = form.cleaned_data['h']
            error_deseado = form.cleaned_data['error_deseado']
            try:
                tabla, pasos = richardson_derivative(funcion, x, h, error_deseado)
                if tabla:
                    resultado_final = tabla[-1]['resultado']
            except Exception as e:
                error = str(e)
    else:
        form = RichardsonForm()

    return render(request, 'richardson_app/index.html', {
        'form': form,
        'tabla': tabla,
        'pasos': pasos,
        'resultado_final': resultado_final,
        'error': error,
    })

@login_required
def home_info(request):
    return render(request, 'metodo_Richardson.html')