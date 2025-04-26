from django.contrib import admin
from django.urls import path, include
from accounts.views import home, custom_login  # Asegúrate de importar custom_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', custom_login, name='account_login'),  # Las rutas de allauth
    path('accounts/', include('allauth.urls')),  # Agregamos la ruta de login personalizado
    path('', home, name='home'),  # La ruta para la página de inicio
]
