from django import forms
from .models import Videollamada

class VideollamadaForm(forms.ModelForm):
    class Meta:
        model = Videollamada
        fields = ['es_publica']  # El usuario solo elige si es pública o privada
