from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='blogs/imagenes/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    aprobado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    

class Comentario(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=True)  # si quieres moderación
    respuesta_a = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='respuestas')

    def __str__(self):
        return f'Comentario de {self.autor.username} en {self.blog.titulo}'