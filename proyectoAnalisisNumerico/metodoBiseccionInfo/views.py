from django.shortcuts import render

def home_info(request):
    return render(request, 'informativa_biseccion.html')
