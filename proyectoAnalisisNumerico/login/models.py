from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=50)    
    apellidos = models.CharField(max_length=50)  
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)
    carrera = models.CharField(max_length=100, blank=True)
    carnet = models.CharField(max_length=20, blank=True)
    ciclo = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'Perfil de {self.nombres} {self.apellidos}'
