from django.contrib import admin
from django.urls import path, include
from accounts.views import home, custom_login, perfil_usuario, editar_perfil  # Importamos las vistas necesarias
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', custom_login, name='account_login'),  # Ruta para el login personalizado
    path('accounts/', include('allauth.urls')),  # Agregamos la ruta de login y otras rutas de allauth
    path('perfil/', perfil_usuario, name='perfil'),  # Ruta para la vista de perfil de usuario
    path('perfil/editar/', editar_perfil, name='editar_perfil'),  # Ruta para la vista de editar perfil de usuario
    path('', home, name='home'),  # Ruta para la página de inicio
]
