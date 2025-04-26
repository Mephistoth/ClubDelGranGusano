from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
     username = forms.EmailField(
         label="Correo Electrónico",

        widget=forms.EmailInput(attrs={
            'placeholder': 'Correo electrónico',
            'autocomplete': 'email',
        })
     )
     password = forms.CharField(
         label="Contraseña",

        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'autocomplete': 'current-password',
        })
     )
