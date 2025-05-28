from django.db import models
from django.contrib.auth.models import User

class Videollamada(models.Model):
    titulo = models.CharField(max_length=100)
    enlace = models.URLField()
    creador = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo