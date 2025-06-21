from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Videollamada
from .forms import VideollamadaForm
from django.contrib import messages
from django.http import HttpResponseForbidden
from .utils import generar_token_jitsi

@login_required
def menu(request):
    return render(request, 'videollamadas/menu.html')

@login_required
def crear_sala(request):
    # Límite de 10 salas activas
    num_activas = Videollamada.objects.filter(activa=True).count()
    if num_activas >= 10:
        messages.error(request, "Ya hay 10 salas activas. Por favor cierra alguna antes de crear una nueva.")
        return redirect('videollamadas:lista_salas')

    if request.method == 'POST':
        form = VideollamadaForm(request.POST)
        if form.is_valid():
            sala = form.save(commit=False)
            sala.creador = request.user
            sala.save()
            messages.success(request, f"Sala creada. Código de invitación: {sala.codigo}")
            return redirect('videollamadas:lista_salas')
    else:
        form = VideollamadaForm()

    return render(request, 'videollamadas/crear_sala.html', {'form': form})

@login_required
def eliminar_sala(request, codigo):
    sala = get_object_or_404(Videollamada, codigo=codigo)
    
    if sala.creador != request.user:
        messages.error(request, "No tienes permiso para eliminar esta sala.")
        return redirect('videollamadas:lista_salas')
    
    sala.delete()
    messages.success(request, "Sala eliminada correctamente.")
    return redirect('videollamadas:lista_salas')

@login_required
def lista_salas(request):
    salas = Videollamada.objects.filter(es_publica=True, activa=True).order_by('-fecha_creacion')
    return render(request, 'videollamadas/lista_salas.html', {'salas': salas})

@login_required
def unirse_sala(request):
    if request.method == 'GET' and 'codigo' in request.GET:
        codigo = request.GET['codigo'].strip()
        try:
            sala = Videollamada.objects.get(codigo=codigo)
        except Videollamada.DoesNotExist:
            messages.error(request, "Código de sala no válido.")
            return redirect('videollamadas:unirse_sala')

        if not sala.es_publica and request.user != sala.creador:
            messages.error(request, "Esta sala es privada. No tienes autorización para unirte.")
            return redirect('videollamadas:unirse_sala')

        return redirect('videollamadas:room', codigo=codigo)

    if request.method == 'POST':
        codigo = request.POST.get('codigo', '').strip()
        try:
            sala = Videollamada.objects.get(codigo=codigo)
        except Videollamada.DoesNotExist:
            messages.error(request, "Código de sala no válido.")
            return redirect('videollamadas:unirse_sala')

        if not sala.es_publica and request.user != sala.creador:
            messages.error(request, "Esta sala es privada. No tienes autorización para unirte.")
            return redirect('videollamadas:unirse_sala')

        return redirect('videollamadas:room', codigo=codigo)

    return render(request, 'videollamadas/unirse.html')

@login_required
def room(request, codigo):
    sala = get_object_or_404(Videollamada, codigo=codigo, activa=True)
    if not sala.es_publica and request.user != sala.creador:
        return HttpResponseForbidden("No tienes permiso para acceder a esta sala.")
     # Genera el JWT para este usuario y sala
    token = generar_token_jitsi(sala.codigo, request.user.username)
    # Importa settings para pasar el tenant
    from django.conf import settings

    return render(request, 'videollamadas/room.html', {
        'sala': sala,
        'token': token,
        'JAAS_TENANT': settings.JAAS_TENANT
    })