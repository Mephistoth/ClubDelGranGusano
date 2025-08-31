import os

# 1) Define SETTINGS MODULE antes de TODO
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GranGusano.settings")

# 2) Importa y ejecuta get_asgi_application, cargando así las apps
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

# 3) Ahora las apps están listas: importa Channels y tu routing
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns

# 4) Monta el router ASGI para HTTP y WebSocket
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
