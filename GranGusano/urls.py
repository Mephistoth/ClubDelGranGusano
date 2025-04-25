from django.contrib import admin
from django.urls import path, include
from accounts.views import home, custom_login  # Asegúrate de importar custom_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Las rutas de allauth
    path('login/', custom_login, name='account_login'),  # Agregamos la ruta de login personalizado
    path('', home, name='home'),  # La ruta para la página de inicio
]
