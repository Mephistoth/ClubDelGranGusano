from django.contrib import admin
from django.urls import path, include
from accounts.views import home, custom_login, perfil_usuario, editar_perfil  # Importamos las vistas necesarias
from django.conf import settings
from django.conf.urls.static import static

from chat import views as chat_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', custom_login, name='account_login'),  # Ruta para el login personalizado
    path('accounts/', include('allauth.urls')),  # Agregamos la ruta de login y otras rutas de allauth
    path('perfil/', perfil_usuario, name='perfil'),  # Ruta para la vista de perfil de usuario
    path('perfil/editar/', editar_perfil, name='editar_perfil'),  # Ruta para la vista de editar perfil de usuario
    path('', home, name='home'),  # Ruta para la página de inicio  
    path('chatbot/', include('chatbotcito.urls')),  # Ruta para las vistas de chatbotcito
    path('chat/', chat_views.chat_room, name='chat'),
    
  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
