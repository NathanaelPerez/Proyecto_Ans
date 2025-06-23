import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import pandas as pd
import io
from PIL import Image
from sympy.parsing.sympy_parser import parse_expr
from historial.models import HistorialCalculo

x = sp.symbols('x')

def f_sym_expr(expr):
    """
    Convierte la expresión ascii-math (o similar) a función lambda numérica.
    """
    try:
        sympy_expr = parse_expr(expr, evaluate=True)
        return sp.lambdify(x, sympy_expr, modules='numpy')
    except Exception as e:
        raise ValueError(f"Error al interpretar la expresión: {e}")

def D_h(expr, x_val, h_val, order):
    f = f_sym_expr(expr)
    if order == 1:
        val = (f(x_val + h_val) - f(x_val - h_val)) / (2 * h_val)
    elif order == 2:
        val = (f(x_val + h_val) - 2 * f(x_val) + f(x_val - h_val)) / (h_val ** 2)
    elif order == 3:
        val = (-f(x_val + 3*h_val) + 8*f(x_val + 2*h_val) - 13*f(x_val + h_val)
               + 13*f(x_val - h_val) - 8*f(x_val - 2*h_val) + f(x_val - 3*h_val)) / (8 * h_val**3)
    elif order == 4:
        val = (-f(x_val + 2*h_val) + 16*f(x_val + h_val) - 30*f(x_val)
               + 16*f(x_val - h_val) - f(x_val - 2*h_val)) / (12 * h_val**4)
    else:
        raise ValueError("Orden no soportado. Sólo 1 a 4.")
    return val

def coef_richardson(order):
    """
    Coeficientes para extrapolación Richardson mejorada, 
    basados en la fórmula D ≈ (4*D(h/2) - D(h))/3 (válida para orden 1).
    Para otros órdenes usamos la misma extrapolación como ejemplo.
    """
    # Para todos los órdenes usamos la fórmula clásica:
    return 4, -1, 3  # coef D(h/2), coef D(h), divisor

def solve_extrapolacion_richardson_detallado(expr, x_val, h_val, order):
    df_latex = pd.DataFrame(columns=['Paso', 'Valor'])

    # Paso 1: Mostrar fórmula usada
    formulas = {
        1: r"D(h) = \frac{f(x+h) - f(x-h)}{2h}",
        2: r"D(h) = \frac{f(x+h) - 2f(x) + f(x-h)}{h^2}",
        3: r"D(h) = \frac{-f(x+3h) + 8f(x+2h) - 13f(x+h) + 13f(x-h) - 8f(x-2h) + f(x-3h)}{8 h^3}",
        4: r"D(h) = \frac{-f(x+2h) + 16f(x+h) - 30f(x) + 16f(x-h) - f(x-2h)}{12 h^4}"
    }
    df_latex.loc[len(df_latex)] = [f"Fórmula para la derivada orden {order}", formulas[order]]

    # Paso 2: Mostrar función
    df_latex.loc[len(df_latex)] = ["Función", f"f(x) = {expr}"]

    # Paso 3: Calcular D(h1) y D(h2) con h y h/2
    D_h1 = D_h(expr, x_val, h_val, order)
    D_h2 = D_h(expr, x_val, h_val/2, order)

    # Paso 4: Mostrar cálculo de error relativo
    error_abs = abs(D_h2 - D_h1)
    error_pct = abs(error_abs / D_h1) * 100 if D_h1 != 0 else 0

    df_latex.loc[len(df_latex)] = [
        "Error relativo (%)",
        r"\varepsilon_a = \left|\frac{D(h/2) - D(h)}{D(h/2)}\right| \times 100\% = "
        + f"|{D_h2} - {D_h1}| / |{D_h2}| * 100% = {round(error_pct, 4)}\\%"
    ]

    # Paso 5: Calcular extrapolación Richardson
    c1, c2, divisor = coef_richardson(order)
    D_ext = (c1 * D_h2 + c2 * D_h1) / divisor

    # Paso 6: Mostrar cálculo extrapolación paso a paso
    df_latex.loc[len(df_latex)] = [
        "Extrapolación Richardson",
        f"D \\approx \\frac{{{c1} \\cdot D(h/2) + ({c2}) \\cdot D(h)}}{{{divisor}}}"
    ]
    df_latex.loc[len(df_latex)] = [
        "Sustituyendo valores",
        f"D \\approx \\frac{{{c1} \\cdot {D_h2} + ({c2}) \\cdot {D_h1}}}{{{divisor}}} = {D_ext}"
    ]

    # Resultado final
    df_latex.loc[len(df_latex)] = ["Resultado final", f"{round(D_ext, 12)}"]

    return D_ext, df_latex, round(error_pct, 6)

def graficar_richardson(expr, x_val, h_val, order=1):
    f_lamb = f_sym_expr(expr)
    d_expr = sp.diff(sp.sympify(expr), x, order)
    d_lamb = sp.lambdify(x, d_expr, 'numpy')

    x_vals = np.linspace(x_val - 2, x_val + 2, 400)

    fx_vals = np.array(f_lamb(x_vals))
    dfx_vals = np.array(d_lamb(x_vals))

    if fx_vals.ndim == 0:
        fx_vals = np.full_like(x_vals, fx_vals)
    if dfx_vals.ndim == 0:
        dfx_vals = np.full_like(x_vals, dfx_vals)

    approx_vals = []
    for xi in x_vals:
        try:
            D1 = D_h(expr, xi, h_val, order)
            D2 = D_h(expr, xi, h_val/2, order)
            c1, c2, divisor = coef_richardson(order)
            D_rich = (c1 * D2 + c2 * D1) / divisor
            approx_vals.append(D_rich)
        except Exception:
            approx_vals.append(np.nan)
    approx_vals = np.array(approx_vals)

    if approx_vals.ndim == 0:
        approx_vals = np.full_like(x_vals, approx_vals)

    fig, ax = plt.subplots()
    ax.plot(x_vals, fx_vals, label="f(x)")
    ax.plot(x_vals, dfx_vals, label=f"Derivada analítica orden {order}")
    ax.plot(x_vals, approx_vals, label=f"Richardson aprox. orden {order}", linestyle=':')
    ax.set_title(f"Derivada orden {order} con extrapolación de Richardson")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf




