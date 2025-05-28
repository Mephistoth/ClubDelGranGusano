from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import Videollamada
from .forms import VideollamadaForm
from django.contrib import messages


@user_passes_test(lambda u: u.is_staff)
@login_required


@login_required
@user_passes_test(lambda u: u.is_staff)
def eliminar_videollamada(request, id):
    try:
        videollamada = Videollamada.objects.get(id=id)
        videollamada.delete()
        messages.success(request, "Videollamada eliminada correctamente.")
    except Videollamada.DoesNotExist:
        messages.error(request, "La videollamada no existe.")
    return redirect('videollamadas_lista')



@user_passes_test(lambda u: u.is_staff)
@login_required
def crear_videollamada(request):
    if request.method == 'POST':
        form = VideollamadaForm(request.POST)
        if form.is_valid():
            llamada = form.save(commit=False)
            llamada.creador = request.user
            llamada.save()
            return redirect('videollamadas_lista')
    else:
        form = VideollamadaForm()
    return render(request, 'videollamadas/crear.html', {'form': form})

@login_required
def lista(request):
    videollamadas = Videollamada.objects.all()
    return render(request, 'videollamadas/lista.html', {'videollamadas': videollamadas})
