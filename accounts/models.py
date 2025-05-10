from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='fotos_perfil/', default='fotos_perfil/default.jpg')

    def __str__(self):
        return self.user.username
