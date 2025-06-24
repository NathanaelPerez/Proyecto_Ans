# SolverPlus: Solución de Ejercicios con Métodos Numéricos

![Python-logo](https://img.shields.io/badge/Python-3.10+-blue?logo=python)  
![Django-logo](https://img.shields.io/badge/Django-4.x-green?logo=django)

## 📌 Descripción del Proyecto

**SolverPlus** es una plataforma desarrollada con **Python** y **Django** que permite resolver problemas utilizando métodos numéricos, enfocados en el **método de bisección** y la **extrapolación de Richardson** para derivadas. Está orientada tanto a estudiantes como a docentes que desean comprender y aplicar estos métodos de manera visual, interactiva y fundamentada.

---

## 📂 Contenidos

- [Instalación](#instalación)  
- [Uso](#uso)  
- [Teoría de los Métodos](#teoría-de-los-métodos)  
  - [Método de Bisección](#método-de-bisección)  
  - [Método de Extrapolación de Richardson](#método-de-extrapolación-de-richardson)  
- [Desarrolladores](#desarrolladores)  
- [Licencia](#licencia)

---

## ⚙️ Instalación

Sigue estos pasos para instalar y ejecutar el proyecto localmente:

```bash
# Clona este repositorio
git clone https://github.com/tu_usuario/solverplus.git

# Entra al directorio del proyecto
cd solverplus

# Crea y activa un entorno virtual
python -m venv venv

# En Windows
venv\Scripts\activate

# En Unix/macOS
source venv/bin/activate

# Instala las dependencias
pip install -r requirements.txt

# Realiza las migraciones
python manage.py migrate

# Inicia el servidor de desarrollo
python manage.py runserver
