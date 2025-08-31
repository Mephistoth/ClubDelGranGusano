from django.contrib import admin
from django.urls import path, include
from accounts.views import home, perfil_usuario, editar_perfil
from django.conf import settings
from django.conf.urls.static import static
from chat import views as chat_views
from blogs.views import home, tinymce_image_upload   # <-- Importamos la vista
from accounts.views import eliminar_cuenta

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # allauth maneja login, logout, signup
    path('perfil/', perfil_usuario, name='perfil'),
    path('perfil/editar/', editar_perfil, name='editar_perfil'),
    path('perfil/eliminar/', eliminar_cuenta, name='eliminar_cuenta'),
    path('', home, name='home'),
    path('chatbot/', include('chatbotcito.urls')),
    path('chat/', chat_views.chat_room, name='chat'),
    path('videollamadas/', include('videollamadas.urls', namespace='videollamadas')),
    path('blogs/', include('blogs.urls')),
    path('tinymce/upload/', tinymce_image_upload, name='tinymce_image_upload'),
    path('tinymce/', include('tinymce.urls')), 
    path('', home, name='home'),   



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
