from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .forms import CustomLoginForm, PerfilForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'account/home.html')

# Vista para el login personalizado
def custom_login(request):
    if request.method == 'POST':
        # 1) Pasar request y data para que AuthenticationForm valide
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            # 2) get_user() devuelve el User autenticado
            user = form.get_user()
            login(request, user)
            return redirect('home')
        # 3) si falla, re-render con error
        form.add_error(None, 'El correo o la contraseña no son correctos.')
    else:
        # Siempre pasar request a AuthenticationForm
        form = CustomLoginForm(request)

    return render(request, 'account/login.html', {'form': form})

@login_required
def perfil_usuario(request):
    return render(request, 'account/perfil.html')


# Vista para editar perfil y cambiar contraseña
@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            password1 = form.cleaned_data.get('password1')
            if password1:
                user.set_password(password1)  # Cambiar la contraseña
            user.save()
            form.save()
            update_session_auth_hash(request, user)  # Mantener al usuario autenticado después de cambiar la contraseña
            return redirect('perfil')  # Redirigir al perfil después de editarlo
    else:
        form = PerfilForm(instance=request.user)
    
    return render(request, 'account/editar_perfil.html', {'form': form})

