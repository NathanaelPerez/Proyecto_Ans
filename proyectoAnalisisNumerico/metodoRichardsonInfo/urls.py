from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('informativa-richardson/', views.home_info, name='informativa_Richardson')
]