import matplotlib.pyplot as plt
import base64
from django.shortcuts import render 
import sympy as sp
import numpy as np
import io

def evaluar_funcion(func_str, x_val):
    x = sp.symbols('x')
    expr = sp.sympify(func_str)
    return float(expr.evalf(subs={x: x_val}))

def funcion_latex_con_valor(funcion_latex, x_val):
    return funcion_latex.replace('x', f'({x_val:.4f})')

def metodo_biseccion(request):
    funcion = None
    resultado = None
    iteraciones = []
    grafica = None
    error_abs = None

    if request.method == 'POST':
        funcion = request.POST.get('funcion')
        xl = float(request.POST.get('xl'))
        xu = float(request.POST.get('xu'))
        ea = float(request.POST.get('ea'))

        x = sp.symbols('x')
        funcion_simbolica = sp.sympify(funcion)
        funcion_latex = sp.latex(funcion_simbolica)

        iter_max = 50
        iter_count = 0
        xr = xl
        ea_actual = 100
        iteraciones = []

        while ea_actual > ea and iter_count < iter_max:
            xr_old = xr
            xr = (xl + xu) / 2
            f_xl = evaluar_funcion(funcion, xl)
            f_xr = evaluar_funcion(funcion, xr)

            xl_iter = xl
            xu_iter = xu

            producto = f_xl * f_xr

            if producto < 0:
                razon = f"""<p>
                \\( f(x_L) \\cdot f(x_R) = {f_xl:.4f} \\cdot {f_xr:.4f} = {producto:.4f} < 0 \\Rightarrow \\)
                la raíz está entre \\( x_L \\) y \\( x_R \\) <br>
                <strong>Entonces:</strong> \\( x_U = x_R = {xr:.4f} \\)
                </p>"""
                xu = xr
            elif producto > 0:
                razon = f"""<p>
                \\( f(x_L) \\cdot f(x_R) = {f_xl:.4f} \\cdot {f_xr:.4f} = {producto:.4f} > 0 \\Rightarrow \\)
                la raíz está entre \\( x_R \\) y \\( x_U \\) <br>
                <strong>Entonces:</strong> \\( x_L = x_R = {xr:.4f} \\)
                </p>"""
                xl = xr
            else:
                razon = f"""<p>
                \\( f(x_L) \\cdot f(x_R) = {f_xl:.4f} \\cdot {f_xr:.4f} = 0 \\Rightarrow \\)
                Se ha encontrado la raíz exacta.
                </p>"""

            iter_count += 1

            if iter_count > 1:
                ea_actual = abs((xr - xr_old) / xr) * 100
            else:
                ea_actual = 100

            f_xl_iter = evaluar_funcion(funcion, xl_iter)
            f_xu_iter = evaluar_funcion(funcion, xu_iter)

            proceso_latex = f"""
                <p>
                \\( \\mathbf{{x_L =}} {xl_iter:.4f} \\) <br>
                \\( \\mathbf{{f(x_L)}} = f({xl_iter:.4f}) = {funcion_latex_con_valor(funcion_latex, xl_iter)} = {f_xl_iter:.4f} \\)
                </p>

                <p>
                \\( \\mathbf{{x_U =}} {xu_iter:.4f} \\) <br>
                \\( \\mathbf{{f(x_U)}} = f({xu_iter:.4f}) = {funcion_latex_con_valor(funcion_latex, xu_iter)} = {f_xu_iter:.4f} \\)
                </p>

                <p>
                \\( \\mathbf{{x_R}} = \\frac{{{xl_iter:.4f} + {xu_iter:.4f}}}{{2}} = {xr:.4f} \\)
                </p>

                <p>
                \\( \\mathbf{{f(x_R)}} = f({xr:.4f}) = {funcion_latex_con_valor(funcion_latex, xr)} = {f_xr:.4f} \\)
                </p>

                <p>
                \\( \\mathbf{{Error}} = \\left| \\frac{{{xr:.4f} - {xr_old:.4f}}}{{{xr:.4f}}} \\right| \\times 100 = {ea_actual:.4f} \\% \\)
                </p>
            """

            proceso_latex += razon

            iteraciones.append({
                'iter': iter_count,
                'xl': xl_iter,
                'xu': xu_iter,
                'xr': xr,
                'f_xl': f_xl,
                'f_xu': f_xu_iter,
                'f_xr': f_xr,
                'ea': ea_actual,
                "proceso": proceso_latex,
            })

        resultado = xr

        if request.user.is_authenticated:
            x_vals = np.linspace(xl - 1, xu + 1, 400)
            y_vals = []
            for x_val in x_vals:
                try:
                    y = evaluar_funcion(funcion, x_val)
                except:
                    y = np.nan
                y_vals.append(y)

            plt.figure(figsize=(8,4))
            plt.axhline(0, color='black')
            plt.plot(x_vals, y_vals, label='f(x)')
            if iteraciones:
                ultima = iteraciones[-1]
                plt.scatter(ultima['xr'], ultima['f_xr'], color='red', label='Resultado')
            plt.title('Método de Bisección')
            plt.xlabel('x')
            plt.ylabel('f(x)')
            plt.legend()

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            buf.seek(0)
            image_png = buf.getvalue()
            grafica = base64.b64encode(image_png).decode('utf-8')

    context = {
        'resultado': resultado,
        'iteraciones': iteraciones if request.user.is_authenticated else [],
        'grafica': grafica,
        'funcion': request.POST.get('funcion', '') if request.method == 'POST' else '',
        'xl': request.POST.get('xl', '') if request.method == 'POST' else '',
        'xu': request.POST.get('xu', '') if request.method == 'POST' else '',
        'ea': request.POST.get('ea', '') if request.method == 'POST' else '',
        'num_iter': len(iteraciones),
        'logeado': request.user.is_authenticated,
    }

    return render(request, 'metodoBiseccion.html', context)
