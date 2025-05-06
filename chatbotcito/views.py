from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '').lower()

        # Respuestas simples (puedes ampliarlas luego)
        if "lombrices" in user_message:
            response = "Las lombrices californianas son excelentes para hacer compostaje."
        elif "compostaje" in user_message:
            response = "El compostaje es el proceso de descomposición de la materia orgánica."
        elif "alimentación" in user_message:
            response = "Las lombrices comen restos vegetales, papel y cartón húmedo."
        else:
            response = "No entendí tu pregunta. Pregúntame sobre lombrices, compostaje o alimentación."

        return JsonResponse({'response': response})
    else:
        return JsonResponse({'response': 'Método no permitido.'}, status=405)