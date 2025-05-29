from django import forms
from .models import Blog
from ckeditor.widgets import CKEditorWidget  # Si usas CKEditor

class BlogForm(forms.ModelForm):
    contenido = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Blog
        fields = ['titulo', 'contenido', 'imagen', 'video_url']