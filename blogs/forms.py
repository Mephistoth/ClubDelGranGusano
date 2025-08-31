from django import forms
from .models import Blog
from ckeditor.widgets import CKEditorWidget  # Si usas CKEditor
from .models import Comentario

class BlogForm(forms.ModelForm):
    contenido = forms.CharField(widget=CKEditorWidget())

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