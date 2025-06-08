from django.contrib import admin
from django.urls import path, include
from accounts.views import home, perfil_usuario, editar_perfil
from django.conf import settings
from django.conf.urls.static import static
from chat import views as chat_views

from videollamadas import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('videollamadas/', include('videollamadas.urls', namespace='videollamadas')),
    path('accounts/', include('allauth.urls')),  # allauth maneja login, logout, signup
    path('perfil/', perfil_usuario, name='perfil'),
    path('perfil/editar/', editar_perfil, name='editar_perfil'),
    path('', home, name='home'),
    path('chatbot/', include('chatbotcito.urls')),
    path('chat/', chat_views.chat_room, name='chat'),
    path('blogs/', include('blogs.urls')),

    path('crear/', views.crear_sala, name='crear_sala'),
    path('salas/', views.lista_salas, name='lista_salas'),
    path('unirse/', views.unirse_sala, name='unirse_sala'),
    path('room/<str:codigo>/', views.room, name='room'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
