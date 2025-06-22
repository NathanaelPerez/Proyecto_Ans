from django.db import models
from django.contrib.auth.models import User

class HistorialCalculo(models.Model):
    METODOS = [
        ('biseccion', 'Bisección'),
        ('richardson', 'Richardson'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    metodo = models.CharField(max_length=20, choices=METODOS)
    funcion = models.TextField()
    resultado = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.metodo} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"
