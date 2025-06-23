import matplotlib.pyplot as plt
import base64
from django.shortcuts import render 
import sympy as sp
import numpy as np
import io
from historial.models import HistorialCalculo 
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
import matplotlib.pyplot as plt
import sympy as sp
import numpy as np
import io
import base64
import re

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

    # Obtener parámetros según método
    if request.method == 'POST':
        funcion = request.POST.get('funcion')
        xl_str = request.POST.get('xl')
        xu_str = request.POST.get('xu')
        ea_str = request.POST.get('ea')
    else:
        funcion = request.GET.get('funcion')
        xl_str = request.GET.get('xl')
        xu_str = request.GET.get('xu')
        ea_str = request.GET.get('ea')

    # Solo continuar si todos los datos están presentes
    if funcion and xl_str and xu_str and ea_str:
        try:
            xl = float(xl_str)
            xu = float(xu_str)
            ea = float(ea_str)

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
            else:
                grafica = None

            # Guardar en historial solo si el usuario está autenticado y es POST
            if request.method == 'POST' and request.user.is_authenticated:
                try:
                    HistorialCalculo.objects.create(
                        usuario=request.user,
                        metodo='Bisección',
                        expr=funcion,
                        xl=xl_str,
                        xu=xu_str,
                        ea=ea_str,
                        resultado=str(round(resultado, 12)),
                    )
                except Exception:
                    pass

        except Exception as e:
            # Puedes pasar error al contexto o manejarlo aquí
            resultado = None
            iteraciones = []
            grafica = None

    context = {
        'resultado': resultado,
        'iteraciones': iteraciones if request.user.is_authenticated else [],
        'grafica': grafica,
        'funcion': funcion or '',
        'xl': xl_str or '',
        'xu': xu_str or '',
        'ea': ea_str or '',
        'num_iter': len(iteraciones),
        'logeado': request.user.is_authenticated,
    }

    return render(request, 'metodoBiseccion.html', context)

# Utilidad para convertir LaTeX a imagen
def latex_formula_to_image(latex_formula):
    plt.rcParams['text.usetex'] = False
    fig = plt.figure(figsize=(0.01, 0.01))
    plt.text(0, 0, f"${latex_formula}$", fontsize=14)
    plt.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=150, transparent=True)
    plt.close(fig)
    buf.seek(0)
    return buf

# Extraer fórmulas de una cadena HTML con LaTeX MathJax
def extraer_formulas(latex_html):
    return re.findall(r'\\\((.*?)\\\)', latex_html)

# Vista para generar PDF del método de Bisección
def descargar_pdf_biseccion(request):
    funcion = request.GET.get("funcion", "")
    try:
        xl = float(request.GET.get("xl"))
        xu = float(request.GET.get("xu"))
        ea = float(request.GET.get("ea"))
    except:
        return HttpResponse("Parámetros inválidos", status=400)

    # Importar y ejecutar método bisección reutilizando lógica
    from .views import evaluar_funcion, funcion_latex_con_valor  # asegúrate que esté en el mismo módulo

    x = sp.symbols('x')
    funcion_sym = sp.sympify(funcion)
    funcion_latex = sp.latex(funcion_sym)

    iter_max = 50
    iteraciones = []
    iter_count = 0
    xr = xl
    ea_actual = 100

    while ea_actual > ea and iter_count < iter_max:
        xr_old = xr
        xr = (xl + xu) / 2
        f_xl = evaluar_funcion(funcion, xl)
        f_xr = evaluar_funcion(funcion, xr)
        xl_iter = xl
        xu_iter = xu
        producto = f_xl * f_xr

        if producto < 0:
            razon = f"f(x_L) * f(x_R) = {f_xl:.4f} * {f_xr:.4f} = {producto:.4f} < 0 ⇒ x_U = x_R = {xr:.4f}"
            xu = xr
        elif producto > 0:
            razon = f"f(x_L) * f(x_R) = {f_xl:.4f} * {f_xr:.4f} = {producto:.4f} > 0 ⇒ x_L = x_R = {xr:.4f}"
            xl = xr
        else:
            razon = f"f(x_L) * f(x_R) = 0 ⇒ raíz exacta"
            ea_actual = 0

        iter_count += 1
        ea_actual = abs((xr - xr_old) / xr) * 100 if iter_count > 1 else 100

        f_xl_iter = evaluar_funcion(funcion, xl_iter)
        f_xu_iter = evaluar_funcion(funcion, xu_iter)

        proceso_latex = f"""
            \\( x_L = {xl_iter:.4f} \\)\\
            \\( f(x_L) = {f_xl_iter:.4f} \\)\\
            \\( x_U = {xu_iter:.4f} \\)\\
            \\( f(x_U) = {f_xu_iter:.4f} \\)\\
            \\( x_R = \\frac{{{xl_iter:.4f} + {xu_iter:.4f}}}{{2}} = {xr:.4f} \\)\\
            \\( f(x_R) = {f_xr:.4f} \\)\\
            \\( Error = {ea_actual:.4f}\\% \\)\\
            \\( {razon} \\)
        """

        iteraciones.append({
            "iter": iter_count,
            "proceso": proceso_latex,
            "xr": xr,
            "f_xr": f_xr
        })

    # === Generar gráfica ===
    x_vals = np.linspace(xl - 1, xu + 1, 400)
    y_vals = [evaluar_funcion(funcion, xv) if np.isfinite(evaluar_funcion(funcion, xv)) else np.nan for xv in x_vals]

    plt.figure(figsize=(6, 3))
    plt.axhline(0, color='black')
    plt.plot(x_vals, y_vals, label='f(x)')
    plt.scatter(xr, evaluar_funcion(funcion, xr), color='red', label='Raíz aproximada')
    plt.title('Gráfica de f(x)')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    graf_buf = io.BytesIO()
    plt.savefig(graf_buf, format='png', bbox_inches='tight', dpi=150)
    plt.close()
    graf_buf.seek(0)

    # === Crear PDF ===
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Método de Bisección - Paso a Paso", styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Función f(x) = {funcion}", styles["Normal"]))
    elements.append(Paragraph(f"xl = {xl}", styles["Normal"]))
    elements.append(Paragraph(f"xu = {xu}", styles["Normal"]))
    elements.append(Paragraph(f"Error permitido (%) = {ea}", styles["Normal"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Resultado final (xr): {round(xr, 6)}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Insertar imagen de gráfica
    elements.append(Paragraph("Gráfica de la función:", styles["Heading2"]))
    elements.append(Spacer(1, 8))
    elements.append(RLImage(graf_buf, width=400, height=200))
    elements.append(Spacer(1, 12))

    # Insertar imágenes de cada paso
    for it in iteraciones:
        elements.append(Paragraph(f"Iteración {it['iter']}:", styles["Heading3"]))
        formulas = extraer_formulas(it["proceso"])
        for formula in formulas:
            try:
                img_buf = latex_formula_to_image(formula)
                img = RLImage(img_buf)
                img._restrictSize(100, 100)
                elements.append(img)
                elements.append(Spacer(1, 4))
            except:
                elements.append(Paragraph(formula, styles["Normal"]))
        elements.append(Spacer(1, 12))

    doc.build(elements)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Ejercicio_Biseccion_paso_a_paso.pdf"'
    return response