from django import forms
from .models import Videollamada

class VideollamadaForm(forms.ModelForm):
    class Meta:
        model = Videollamada
        fields = ['titulo', 'enlace']
