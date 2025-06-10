from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_blogs, name='lista_blogs'),
    path('crear/', views.crear_blog, name='crear_blog'),
    path('<int:blog_id>/', views.detalle_blog, name='detalle_blog'),
    # Rutas para moderación
    path('admin-blogs/', views.moderar_blogs, name='moderar_blogs'),
    path('admin-blogs/aprobar/<int:blog_id>/', views.aprobar_blog, name='aprobar_blog'),
    path('admin-blogs/rechazar/<int:blog_id>/', views.rechazar_blog, name='rechazar_blog'),
    path('blog/<int:blog_id>/eliminar/', views.eliminar_blog, name='eliminar_blog'),

]