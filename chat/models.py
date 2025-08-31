from django.db import models
from django.conf import settings

class Message(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']  # orden cronológico

    def __str__(self):
        return f"{self.user or 'Invitado'}: {self.content[:20]}"