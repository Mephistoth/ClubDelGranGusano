from django import forms
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from .models import Profile

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30,
        label="Nombre",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre'
        })
    )
    
    def save (self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data ['first_name']
        user.save()
        return user

class CustomLoginForm(AuthenticationForm):
     password = forms.CharField(
         label="Contraseña",

        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'autocomplete': 'current-password',
        })
     )


class PerfilForm(forms.ModelForm):
    # Añadimos los campos para la edición del perfil
    # username = forms.CharField(max_length=150,label="Nombre de usuario",required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, label="Nombre", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, label="Apellido", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    
    # Campos para cambiar la contraseña
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

    # Campo para la foto de perfil
    foto = forms.ImageField(label='Foto de perfil', required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        # fields = ['username','first_name', 'last_name', 'email']
        fields = ['first_name', 'last_name']

    # Validación para la contraseña
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        
        return cleaned_data

    def save(self, commit=True):
         # Guardar el usuario
        user = super().save(commit=commit)
        # Guardar la foto de perfil
        foto = self.cleaned_data.get('foto')

        if foto:
            # Asegúrate de que el perfil del usuario existe
            profile, created = Profile.objects.get_or_create(user=user)
            profile.foto = foto
            profile.save()

        if self.cleaned_data.get('password1'):
            user.set_password(self.cleaned_data.get('password1'))
            user.save()

        return user