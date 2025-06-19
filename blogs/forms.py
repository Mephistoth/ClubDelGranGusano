from django import forms
from .models import Blog
# from ckeditor.widgets import CKEditorWidget # <--- ¡Borra esta importación!
from .models import Comentario # Asegúrate de que Comentario esté importado o definido

class BlogForm(forms.ModelForm):
    # contenido = forms.CharField(widget=CKEditorWidget()) # <--- ¡Borra esta línea!
    # El campo 'contenido' ahora es un HTMLField en el modelo, y TinyMCE lo manejará automáticamente.

    class Meta:
        model = Blog
        fields = ['titulo', 'contenido', 'imagen', 'video_url']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe un comentario...'})
        }