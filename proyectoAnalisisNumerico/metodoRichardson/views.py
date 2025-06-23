import base64
from django.shortcuts import render
from . import richardson
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from PIL import Image
import io
import matplotlib.pyplot as plt
import sympy as sp
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet
from .richardson import solve_extrapolacion_richardson_detallado

def calcular_richardson(request):
    if request.method == 'POST':
        expr = request.POST.get('expr', '')
        x_val = request.POST.get('x_val', '')
        h_val = request.POST.get('h_val', '')
        order = request.POST.get('order', '1')

        # Validar que no vengan vacíos o incorrectos
        try:
            x_val = float(x_val)
            h_val = float(h_val)
            order = int(order)
        except ValueError:
            return render(request, 'metodo_Richardson.html', {
                'error': 'Valores inválidos para x, h o el orden.',
                'expr': expr,
                'x_val': x_val,
                'h_val': h_val,
                'order': order,
            })

        if order < 1 or order > 4:
            return render(request, 'metodo_Richardson.html', {
                'error': 'El orden debe ser entre 1 y 4.',
                'expr': expr,
                'x_val': x_val,
                'h_val': h_val,
                'order': order,
            })

        try:
            resultado, latex, error = richardson.solve_extrapolacion_richardson_detallado(expr, x_val, h_val, order)
        except ValueError as e:
            return render(request, 'metodo_Richardson.html', {
                'error': str(e),
                'expr': expr,
                'x_val': x_val,
                'h_val': h_val,
                'order': order,
            })

        img_buffer = richardson.graficar_richardson(expr, x_val, h_val, order)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

        return render(request, 'metodo_Richardson.html', {
            'resultado': round(resultado, 12),
            'latex': latex.values.tolist(),
            'grafico': img_base64,
            'expr': expr,
            'x_val': x_val,
            'h_val': h_val,
            'order': order,
            'error': error,
        })

    return render(request, 'metodo_Richardson.html')

def latex_formula_to_image(latex_formula):
    """Convierte una fórmula LaTeX a imagen PNG en memoria (BytesIO)."""
    plt.rcParams['text.usetex'] = False
    fig = plt.figure(figsize=(0.01, 0.01))
    plt.text(0, 0, f"${latex_formula}$", fontsize=14)
    plt.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=150, transparent=True)
    plt.close(fig)
    buf.seek(0)
    return buf


def descargar_pdf_richardson(request):
    if request.method == 'GET':
        expr = request.GET.get('expr', '')
        x_val = float(request.GET.get('x_val', 0))
        h_val = float(request.GET.get('h_val', 0.1))
        orden = int(request.GET.get('orden', 1))

        resultado, latex_df, error = solve_extrapolacion_richardson_detallado(expr, x_val, h_val, orden)

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        doc.title = "Ejercicio Richardson paso a paso"

        styles = getSampleStyleSheet()
        normal_style = styles["Normal"]
        heading_style = styles["Heading1"]
        heading_style.alignment = 1

        elements = []
        elements.append(Paragraph("Método de Richardson - Paso a Paso", heading_style))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Función f(x) = {expr}", normal_style))
        elements.append(Paragraph(f"Valor de x = {x_val}", normal_style))
        elements.append(Paragraph(f"Valor de h inicial = {h_val}", normal_style))
        elements.append(Paragraph(f"Orden de la derivada = {orden}", normal_style))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Resultado final de la derivada: <b>{round(resultado, 6)}</b>", normal_style))
        elements.append(Spacer(1, 12))

        def add_formula(parrafo, formula_latex, width_px=100, height_px=100):
            elements.append(Paragraph(parrafo, normal_style))
            try:
                img_buf = latex_formula_to_image(formula_latex)
                img = RLImage(img_buf)
                img._restrictSize(width_px, height_px)
                elements.append(img)
            except Exception:
                elements.append(Paragraph(formula_latex, normal_style))
            elements.append(Spacer(1, 8))

        for _, row in latex_df.iterrows():
            paso = row['Paso']
            valor = row['Valor']
            if paso.lower() == "sustituyendo valores":
                add_formula(f"<b>{paso}:</b>", valor, width_px=180, height_px=180)
            else:
                add_formula(f"<b>{paso}:</b>", valor, width_px=100, height_px=100)

        doc.build(elements)
        buffer.seek(0)

        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Ejercicio_Richardson_paso_a_paso.pdf"'
        return response

    return HttpResponse("Método no permitido", status=405)
