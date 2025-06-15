from django.shortcuts import render
from sympy import symbols, sympify, lambdify
import math

def index(request):
    if request.method == 'GET' and 'x' in request.GET and 'h' in request.GET and 'tolerancia' in request.GET and 'funcion' in request.GET:
        try:
            # Recoger parámetros
            f_str = request.GET.get('funcion')
            x = float(request.GET.get('x'))
            h = float(request.GET.get('h'))
            tolerancia = float(request.GET.get('tolerancia'))

            # Símbolo y función evaluable
            x_sym = symbols('x')
            f_expr = sympify(f_str)
            f = lambdify(x_sym, f_expr, 'math')

            tabla = []
            pasos = []
            i = 0
            error = float('inf')
            D_anterior = 0

            while error > tolerancia:
                h_i = h / (2 ** i)
                f_x_plus = f(x + h_i)
                f_x_minus = f(x - h_i)
                D = (f_x_plus - f_x_minus) / (2 * h_i)

                if i == 0:
                    R = D
                    error = float('inf')
                else:
                    R = D + (D - D_anterior) / (4 ** 1 - 1)  # p=1 para centradas
                    error = abs((R - D_anterior) / R) * 100

                tabla.append({
                    'iteracion': i + 1,
                    'h': round(h_i, 6),
                    'D': round(D, 6),
                    'R': round(R, 6) if i > 0 else None,
                    'error': round(error, 6) if i > 0 else None
                })

                pasos.append({
                    'iteracion': i + 1,
                    'diferencias': f"D = (f({x}+{h_i}) - f({x}-{h_i})) / (2*{h_i}) = ({f_x_plus} - {f_x_minus}) / {2 * h_i} = {D}",
                    'richardson': f"R = D + (D - D_prev) / (4^1 - 1) = {D} + ({D} - {D_anterior}) / 3 = {R}" if i > 0 else "Primera iteración, sin extrapolación",
                    'error': f"Error relativo = |R - D_prev| / |R| * 100 = |{R} - {D_anterior}| / |{R}| * 100 = {error:.6f}%" if i > 0 else "No se calcula en la primera iteración"
                })

                if error <= tolerancia:
                    break

                D_anterior = D
                i += 1

            return render(request, 'metodo_Richardson.html', {
                'tabla': tabla,
                'pasos': pasos,
                'resultado': round(R, 6),
                'x': x,
                'tolerancia': tolerancia,
                'funcion': f_str
            })

        except Exception as e:
            return render(request, 'metodo_Richardson.html', {
                'error': f'Ocurrió un error: {str(e)}'
            })

    return render(request, 'metodo_Richardson.html')
