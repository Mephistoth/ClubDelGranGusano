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