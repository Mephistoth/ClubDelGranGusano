from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import PerfilForm
from .models import Profile
import cloudinary.uploader


def home(request):
    return render(request, 'account/home.html')

@login_required
def perfil_usuario(request):
    return render(request, 'account/perfil.html')

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)

            # Cambiar contraseña si se proporcionó
            password1 = form.cleaned_data.get('password1')
            if password1:
                user.set_password(password1)

            user.save()

            # Procesar foto de perfil solo si hay archivo válido
            foto = form.cleaned_data.get('foto')
            if foto and foto.size:
                profile, _ = Profile.objects.get_or_create(user=user)
                upload_result = cloudinary.uploader.upload(foto)
                profile.foto = upload_result.get('secure_url', '')
                profile.save()

            update_session_auth_hash(request, user)  # mantener sesión activa tras cambio de contraseña
            return redirect('perfil')
    else:
        form = PerfilForm(instance=request.user)

    return render(request, 'account/editar_perfil.html', {'form': form})

@login_required
def eliminar_cuenta(request):
    if request.method == 'POST':
        user = request.user
        email = user.email
        username = user.username

        # Enviar correo notificando
        send_mail(
            subject='Cuenta eliminada',
            message=f'Hola {username}, tu cuenta en ClubDelGranGusano ha sido eliminada.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )

        user.delete()
        logout(request)
        return redirect('home')

    # Si es GET, redirige a perfil
    return redirect('perfil')