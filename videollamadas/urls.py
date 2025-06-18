from django.urls import path
from . import views

app_name = 'videollamadas'
urlpatterns = [
    path('crear/', views.crear_sala, name='crear_sala'),
    path('salas/', views.lista_salas, name='lista_salas'),
    path('unirse/', views.unirse_sala, name='unirse_sala'),
    path('room/<str:codigo>/', views.room, name='room'),
]
