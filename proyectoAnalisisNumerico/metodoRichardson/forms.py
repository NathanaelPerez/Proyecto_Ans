from django import forms

class RichardsonForm(forms.Form):
    function = forms.CharField(label='Función f(x)', max_length=100)
    x = forms.FloatField(label='Valor de x')
    h = forms.FloatField(label='Valor inicial de h')
    error_deseado = forms.FloatField(label='Error deseado (%)')
