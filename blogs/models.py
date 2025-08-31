# blogs/models.py
from django.db import models
from django.contrib.auth.models import User # <-- Asegúrate de que User esté importado
from tinymce.models import HTMLField # <--- ¡Importa el HTMLField de TinyMCE!
from django.db import models

class EmailBloqueado(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

class Blog(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = HTMLField(blank=True, null=True) # <--- ¡Usa HTMLField para el contenido!
    imagen = models.ImageField(upload_to='blogs/imagenes/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    aprobado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE) # <-- Este es el que requiere un usuario logueado
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=True)
    respuesta_a = models.ForeignKey(
        'self',        # Apunta a la misma clase Comentario
        null=True,     # Puede ser nulo (comentario de nivel superior)
        blank=True,    # Puede estar en blanco en formularios
        on_delete=models.CASCADE,
        related_name='respuestas' # Permite acceder a las respuestas: comentario.respuestas.all()
    )

    def __str__(self):
        return f'Comentario de {self.autor.username} en {self.blog.titulo}'
    
    