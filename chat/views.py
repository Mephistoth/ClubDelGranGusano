# chat/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def chat_room(request):
    # Obtener los últimos 50 mensajes y mostrarlos cronológicamente
    messages = Message.objects.all().order_by('-timestamp')[:50]
    messages = list(reversed(messages))
    return render(request, 'chat/chat.html', {
        'messages': messages,
        'user': request.user
    })