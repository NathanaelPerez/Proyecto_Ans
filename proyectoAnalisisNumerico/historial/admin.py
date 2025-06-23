from django.contrib import admin
from .models import HistorialCalculo

@admin.register(HistorialCalculo)
class HistorialCalculoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'metodo', 'fecha', 'resultado')
    list_filter = ('metodo', 'fecha')
    search_fields = ('usuario__username', 'funcion', 'expr')
