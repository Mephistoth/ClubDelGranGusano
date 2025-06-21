import uuid
from django.db import models
from django.contrib.auth.models import User

class Videollamada(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)        # Fecha y hora de creación automática:contentReference[oaicite:0]{index=0}}
    nombre = models.CharField("Nombre de la sala", max_length=100)
    creador = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario que crea la sala:contentReference[oaicite:1]{index=1}
    codigo = models.CharField(
        max_length = 8,
        unique = True,
        blank = True)
    es_publica = models.BooleanField(default=True)              # Si la sala es pública o privada
    activa = models.BooleanField(default=True)              # Indicador de sala activa

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = uuid.uuid4().hex[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Videollamada {self.codigo}"