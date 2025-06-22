from django.urls import path
from . import views

urlpatterns = [
    path('', views.historial_view, name='ver_historial'),
]
