from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista, name='videollamadas_lista'),
    path('crear/', views.crear_videollamada, name='crear_videollamada'),
    path('eliminar/<int:id>/', views.eliminar_videollamada, name='eliminar_videollamada'),
]
