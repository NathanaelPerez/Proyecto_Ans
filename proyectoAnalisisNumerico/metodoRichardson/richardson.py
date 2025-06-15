from sympy import symbols, sympify, lambdify
import math

def metodo_richardson(f_str, x, h, tolerancia):
    x_sym = symbols('x')
    f_expr = sympify(f_str)
    f = lambdify(x_sym, f_expr, 'math')

    tabla = []
    pasos = []
    i = 0
    error = float('inf')
    D_anterior = 0

    while error > tolerancia:
        h_i = h / (2**i)

        # Diferencias centradas
        f_x_plus = f(x + h_i)
        f_x_minus = f(x - h_i)
        D = (f_x_plus - f_x_minus) / (2 * h_i)

        # Extrapolación de Richardson
        if i == 0:
            R = D
            error = float('inf')
        else:
            R = D + (D - D_anterior) / (4**1 - 1)  # p = 1 para centradas
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
            'diferencias': f"D = (f({x}+{h_i}) - f({x}-{h_i})) / (2*{h_i}) = ({f_x_plus} - {f_x_minus}) / {2*h_i} = {D}",
            'richardson': f"R = D + (D - D_prev) / (4^1 - 1) = {D} + ({D} - {D_anterior}) / 3 = {R}" if i > 0 else "Primera iteración, sin extrapolación",
            'error': f"Error relativo = |R - D_prev| / |R| * 100 = |{R} - {D_anterior}| / |{R}| * 100 = {error:.6f}%" if i > 0 else "No se calcula en la primera iteración"
        })

        if error <= tolerancia:
            break

        D_anterior = D
        i += 1

    return tabla, pasos, R
