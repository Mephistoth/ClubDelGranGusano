from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .chatbot_data import knowledge_base

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '').lower().strip()

        respuesta = "No entendí tu pregunta. Intenta con otra o sé más específico."

        for pregunta, respuesta_posible in knowledge_base.items():
            if pregunta in user_message:
                respuesta = respuesta_posible
                break

        return JsonResponse({'response': respuesta})
    else:
        return JsonResponse({'response': 'Método no permitido.'}, status=405)
