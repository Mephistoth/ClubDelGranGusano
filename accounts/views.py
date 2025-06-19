from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from .forms import PerfilForm
from django.contrib.auth.decorators import login_required


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

            # Mantener la lógica de la contraseña
            password1 = form.cleaned_data.get('password1')
            if password1:
                user.set_password(password1)

            user.save()

            # Guardar foto y demás (usando form.save para subir foto)
            form.save()

            update_session_auth_hash(request, user)
            return redirect('perfil')
    else:
        form = PerfilForm(instance=request.user)
    return render(request, 'account/editar_perfil.html', {'form': form})

