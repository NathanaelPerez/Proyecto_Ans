from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('sobre-Nosotros/', views.index, name='sobre_Nosotros')
]

