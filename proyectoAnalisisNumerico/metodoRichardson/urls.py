from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('metodo-richardson/', views.home_info, name='metodo_richardson')
]