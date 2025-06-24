from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('metodo-richardson/', views.calcular_richardson, name='metodo_richardson'),
    path('descargar_pdf/', views.descargar_pdf_richardson, name='descargar_pdf'),

]