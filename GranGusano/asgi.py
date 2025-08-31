import os

# 1) Establece la variable de entorno ANTES de cualquier import de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GranGusano.settings")

# 2) Ahora importa y obtén la app ASGI de Django
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

# 3) Importa Channels sólo después de cargar Django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing  # tu routing de WebSocket

# 4) Define el router ASGI
application = ProtocolTypeRouter({
    "http": django_asgi_app,      # Maneja todas las peticiones HTTP
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns  # Tus rutas WS
        )
    ),
})