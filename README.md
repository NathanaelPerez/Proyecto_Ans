# SolverPlus

## Proyecto de Solución de Ejercicios con Métodos Numéricos

---

### Descripción del Proyecto

Este proyecto está desarrollado en **Python** y **Django**, y su objetivo es resolver ejercicios utilizando dos métodos numéricos fundamentales:

- **Método de Bisección**
- **Método de Extrapolación de Richardson**

---

### Contenidos

- [Instalación](#instalación)  
- [Uso](#uso)  
- [Teoría de los Métodos](#teoría-de-los-métodos)  
  - [Método de Bisección](#método-de-bisección)  
  - [Método de Extrapolación de Richardson](#método-de-extrapolación-de-richardson)  
- [Integrantes](#integrantes)  
- [Licencia](#licencia)  

---

### Instalación

Para instalar y configurar el proyecto, sigue estos pasos:

```bash
# Clona este repositorio:
git clone https://github.com/tu_usuario/solverplus.git

# Navega al directorio del proyecto:
cd solverplus

# Crea y activa un entorno virtual:
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instala las dependencias:
pip install -r requirements.txt

# Realiza las migraciones:
python manage.py migrate

# Inicia el servidor de desarrollo:
python manage.py runserver
```

### Uso

Abre tu navegador y visita:  
`http://localhost:8000`

Sigue las instrucciones en la interfaz para resolver ejercicios usando los métodos disponibles.

---

### Teoría de los Métodos

#### Método de Bisección

El método de bisección es una técnica numérica para encontrar raíces de una función continua en un intervalo \([a, b]\) donde la función cambia de signo.  
El procedimiento consiste en:

1. Dividir el intervalo por la mitad y evaluar la función en el punto medio \(c = \frac{a+b}{2}\).
2. Determinar en cuál subintervalo \([a,c]\) o \([c,b]\) la función cambia de signo.
3. Repetir el proceso en el subintervalo seleccionado hasta alcanzar la precisión deseada.

Este método garantiza la convergencia a una raíz siempre que la función sea continua y se cumpla la condición del cambio de signo.

---

#### Método de Extrapolación de Richardson

La extrapolación de Richardson es una técnica para mejorar la precisión de aproximaciones numéricas que dependen de un parámetro \(h\) (por ejemplo, tamaño de paso).  
Si se tiene una aproximación \(A(h)\) que varía con \(h\), se puede obtener una mejor estimación combinando \(A(h)\) con valores de \(A\) calculados para diferentes valores de \(h\) mediante la fórmula:

\[
R = \frac{2^p A(h/2) - A(h)}{2^p - 1}
\]

donde \(p\) es el orden del error en la aproximación.  

En este proyecto, se utiliza extrapolación de Richardson para calcular derivadas numéricas con orden de precisión mejorado \(O(h^4)\), lo que permite obtener resultados más precisos con menos error.

---

### Integrantes

- **Pedro David Ramos García**  
  Carnet: RG21057  
  Responsabilidades: Implementación del método de bisección y desarrollo frontend.

- **Kevin Nathanael Granados Pérez**  
  Carnet: GP22006  
  Responsabilidades: Implementación del método de extrapolación de Richardson y pruebas unitarias.

---

### Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).
