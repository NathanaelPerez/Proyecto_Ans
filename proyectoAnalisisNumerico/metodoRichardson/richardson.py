import math

def richardson_derivative(func_str, x, h_inicial, error_deseado):
    from sympy import sympify, Symbol, lambdify

    x_sym = Symbol('x')
    f = sympify(func_str)
    f_lambda = lambdify(x_sym, f, 'math')

    tabla = []
    pasos = []

    h = h_inicial
    iteracion = 1
    resultado_anterior = None
    error_actual = float('inf')

    while error_actual > error_deseado:
        D1 = (f_lambda(x + h) - f_lambda(x - h)) / (2 * h)
        D2 = (f_lambda(x + h / 2) - f_lambda(x - h / 2)) / (2 * (h / 2))

        richardson = D2 + (D2 - D1) / 3

        if resultado_anterior is not None:
            error_actual = abs((richardson - resultado_anterior) / richardson) * 100
        else:
            error_actual = 100

        # Guardamos datos en tabla
        tabla.append({
            'iteracion': iteracion,
            'h': h,
            'D1': D1,
            'D2': D2,
            'resultado': richardson,
            'error': error_actual,
        })

        # Guardamos paso a paso
        pasos.append({
            'iteracion': iteracion,
            'formula': "D2 + (D2 - D1) / 3",
            'datos': {
                'D1': D1,
                'D2': D2,
                'h': h,
            },
            'sustitucion': f"{D2:.10f} + ({D2:.10f} - {D1:.10f}) / 3",
            'resultado': richardson,
            'error': error_actual
        })

        resultado_anterior = richardson
        h /= 2
        iteracion += 1

        if iteracion > 20:  # Por seguridad
            break

    return tabla, pasos
