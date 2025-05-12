from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def crear_o_actualizar_perfil(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # Asegura que el perfil exista y luego guárdalo
        profile, _ = Profile.objects.get_or_create(user=instance)
        profile.save()
