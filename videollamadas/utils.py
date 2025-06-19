import datetime
import jwt
from django.conf import settings

def generar_token_jitsi(nombre_sala, nombre_usuario):
    with open(settings.JAAS_PRIVATE_KEY_PATH, 'r') as f:
        private_key = f.read()

    now = int(datetime.datetime.utcnow().timestamp())

    payload = {
        "aud": "jitsi",
        "iss": "chat",
        "sub": settings.JAAS_TENANT,  # Tu AppID completo
        "room": nombre_sala,
        "iat": now,
        "exp": now + 3600,  # Válido por 1 hora
        "context": {
            "user": {"name": nombre_usuario},
            "features": {}  # Obligatorio aunque esté vacío
        }
    }

    headers = {
        "kid": settings.JAAS_KID,
        "typ": "JWT"
    }

    print("JWT payload:", payload)
    token = jwt.encode(payload, private_key, algorithm="RS256", headers=headers)
    print("JWT token:", token)

    return token