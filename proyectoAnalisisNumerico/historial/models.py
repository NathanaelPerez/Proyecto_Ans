from django.db import models
from django.contrib.auth.models import User

class HistorialCalculo(models.Model):
    METODO_CHOICES = [
        ('biseccion', 'Bisección'),
        ('richardson', 'Extrapolación de Richardson'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='historial_calculos')
    metodo = models.CharField(max_length=20, choices=METODO_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True)

    # Campos para Bisección
    funcion = models.TextField(blank=True, null=True)  # expresion f(x)
    xl = models.FloatField(blank=True, null=True)
    xu = models.FloatField(blank=True, null=True)
    ea = models.FloatField(blank=True, null=True)

    # Campos para Richardson
    expr = models.TextField(blank=True, null=True)
    x_val = models.FloatField(blank=True, null=True)
    h_val = models.FloatField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)

    resultado = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.metodo} - {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}"
