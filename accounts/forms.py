from django import forms
from django.contrib.auth.models import User
from allauth.account.forms import LoginForm
from allauth.account.models import EmailAddress
from .models import Profile
import cloudinary.uploader

# FORMULARIO PERSONALIZADO DE LOGIN
class CustomLoginForm(LoginForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)  # mantiene validaciones internas de allauth

        verified = EmailAddress.objects.filter(
            user=user,
            primary=True,
            verified=True
        ).exists()

        if not verified:
            raise forms.ValidationError(
                "Debes verificar tu correo antes de iniciar sesión.",
                code='email_not_verified'
            )


# FORMULARIO DE PERFIL DE USUARIO MEJORADO
class PerfilForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30, 
        label="Nombre", 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30, 
        label="Apellido", 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    password1 = forms.CharField(
        label="Contraseña nueva",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )

    foto = forms.ImageField(
        label='Foto de perfil', 
        required=False, 
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=commit)
        foto = self.cleaned_data.get('foto')

        if foto:
            profile, created = Profile.objects.get_or_create(user=user)
            # Solo subir a Cloudinary si el archivo no está vacío
            if foto.size > 0:
                upload_result = cloudinary.uploader.upload(foto)
                profile.foto = upload_result.get('secure_url', '')  # Guarda la URL segura
                profile.save()

        if self.cleaned_data.get('password1'):
            user.set_password(self.cleaned_data.get('password1'))
            user.save()

        return user
