from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomLoginForm

def home(request):
    return render(request, 'account/home.html')

# Vista para el login personalizado
def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)  # Asegúrate de que este es tu formulario de login
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None and user.is_active:
                login(request, user)  # Inicia sesión
                return redirect('home')  # Redirige al home
            else:
                form.add_error(None, 'El correo o la contraseña no son correctos.')
    else:
        form = CustomLoginForm()  # Si es un GET, mostramos el formulario vacío

    return render(request, 'account/login.html', {'form': form})