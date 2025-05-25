# videollamada/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def videollamada_room(request, room_name):
    return render(request, 'videollamada/room.html', {
        'room_name': room_name,
    })