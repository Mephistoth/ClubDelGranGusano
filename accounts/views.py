from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomLoginForm

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