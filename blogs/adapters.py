from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError
from .models import EmailBloqueado

class CustomAccountAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        email = super().clean_email(email)
        if EmailBloqueado.objects.filter(email__iexact=email).exists():
            raise ValidationError("Este correo ha sido bloqueado. No puedes registrarte con este email.")
        return email
