<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>SolverPlus - Documentación</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f5f5f5;
      color: #222;
      line-height: 1.6;
      padding: 20px;
      max-width: 900px;
      margin: auto;
    }

    h1, h2 {
      color: #F04770;
    }

    h1 {
      text-align: center;
    }

    code {
      background-color: #eee;
      padding: 2px 4px;
      border-radius: 4px;
      font-family: monospace;
    }

    ul, ol {
      padding-left: 20px;
    }

    .dev {
      background-color: #fff;
      border: 1px solid #ddd;
      padding: 10px;
      margin-top: 10px;
      border-radius: 10px;
    }

    .logos {
      display: flex;
      gap: 20px;
      justify-content: center;
      align-items: center;
      margin-bottom: 20px;
      flex-wrap: wrap;
    }

    .logos img {
      height: 60px;
    }

    a.upload-link {
      display: inline-block;
      margin-top: 10px;
      color: #108AB1;
      text-decoration: underline;
    }
  </style>
</head>
<body>
  <a class="upload-link" href="#" onclick="alert('Aquí irá tu enlace de carga personalizado o funcionalidad en el futuro.')">Subir logo personalizado</a>
  <h1>SolverPlus</h1>
  <p style="text-align: center;"><strong>Plataforma web para resolver ejercicios con métodos numéricos</strong></p>

  <div class="logos">
    <img src="https://www.python.org/static/community_logos/python-logo.png" alt="Logo de Python">
    <img src="https://static.djangoproject.com/img/logos/django-logo-negative.png" alt="Logo de Django">
  </div>

  <h2>📌 Descripción del Proyecto</h2>
  <p><strong>SolverPlus</strong> es una herramienta web desarrollada con <strong>Python</strong> y <strong>Django</strong>, que permite resolver problemas matemáticos aplicando métodos numéricos:</p>
  <ul>
    <li>✅ Método de Bisección</li>
    <li>✅ Método de Extrapolación de Richardson</li>
  </ul>

  <h2>📂 Contenidos</h2>
  <ul>
    <li>Instalación</li>
    <li>Uso</li>
    <li>Teoría de los Métodos</li>
    <li>Desarrolladores</li>
    <li>Licencia</li>
  </ul>

  <h2>⚙️ Instalación</h2>
  <ol>
    <li>Clona el repositorio:<br><code>git clone https://github.com/tu_usuario/tu_repositorio.git</code></li>
    <li>Accede a la carpeta:<br><code>cd tu_repositorio</code></li>
    <li>Crea y activa un entorno virtual:<br>
      <code>python -m venv venv</code><br>
      <code>source venv/bin/activate</code> <em>(en Windows: <code>venv\Scripts\activate</code>)</em>
    </li>
    <li>Instala las dependencias:<br><code>pip install -r requirements.txt</code></li>
    <li>Realiza las migraciones:<br><code>python manage.py migrate</code></li>
    <li>Inicia el servidor:<br><code>python manage.py runserver</code></li>
  </ol>

  <h2>🧪 Uso</h2>
  <p>Abre tu navegador y entra a <code>http://localhost:8000</code>. Desde ahí podrás ingresar los valores y aplicar los métodos paso a paso.</p>

  <h2>📘 Teoría de los Métodos</h2>

  <h3>Método de Bisección</h3>
  <p>Se utiliza para encontrar raíces de funciones continuas <code>f(x)</code> en un intervalo <code>[a, b]</code> donde <code>f(a) * f(b) &lt; 0</code>. En cada iteración, se reduce el intervalo a la mitad hasta converger a la raíz.</p>

  <h3>Método de Extrapolación de Richardson</h3>
  <p>Este método mejora la precisión de aproximaciones numéricas. Se utiliza especialmente en el cálculo de derivadas con diferentes valores de <code>h</code>, aplicando fórmulas como:</p>
  <p><code>R(h) = \frac{4A(h/2) - A(h)}{3}</code></p>
  <p>En este proyecto se utiliza una versión con orden <code>O(h⁴)</code> para derivadas más precisas.</p>

  <h2>👨‍💻 Desarrolladores</h2>
  <div class="dev">
    <strong>Pedro David Ramos García</strong><br>
    Carnet: —<br>
    Responsabilidad: Desarrollo del método de bisección y parte del backend.
  </div>
  <div class="dev">
    <strong>Kevin Nathanel Granados Pérez</strong><br>
    Carnet: —<br>
    Responsabilidad: Desarrollo del método de Richardson y soporte general del sistema.
  </div>

  <h2>🪪 Licencia</h2>
  <p>Este proyecto es de código abierto. Puedes modificar y distribuir según lo permitan sus autores.</p>
</body>
</html>
