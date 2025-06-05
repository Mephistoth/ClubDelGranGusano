from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_blogs, name='lista_blogs'),
    path('crear/', views.crear_blog, name='crear_blog'),
    path('<int:blog_id>/', views.detalle_blog, name='detalle_blog'),
]