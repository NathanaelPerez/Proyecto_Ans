from django.urls import path 
from . import views

urlpatterns = [
    path('metodo-biseccion/', views.metodo_biseccion, name='metodo_biseccion'),
    path('descargar_pdf/', views.descargar_pdf_biseccion, name='descargar_pdf_biseccion'),
]