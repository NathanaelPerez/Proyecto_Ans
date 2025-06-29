"""
URL configuration for proyectoAnalisisNumerico project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
    path('', include('login.urls')),
    path('', include('registro.urls')),
    path('', include('metodoBiseccion.urls')),
    path('', include('metodoBiseccionInfo.urls')),
    path('', include('metodoRichardsonInfo.urls')),
    path('', include('metodoRichardson.urls')),
    path('', include('sobreNosotros.urls')),
    path('historial/', include('historial.urls')),
    path('editar-perfil/', include('editarperfil.urls')),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
