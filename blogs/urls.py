from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_blogs, name='lista_blogs'),
    path('crear/', views.crear_blog, name='crear_blog'),
]