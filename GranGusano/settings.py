from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# ─── CARGA DE .env Y RUTAS ─────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))  # Tu .env actual

# ─── CONFIG. BÁSICA ────────────────────────────────────────────────────────────
SECRET_KEY = os.getenv('SECRET_KEY', 'clave-dev-insegura')
DEBUG     = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*']  # Ajusta en prod si lo deseas

TIME_ZONE = 'America/Santiago'
USE_TZ    = True
USE_I18N  = True
LANGUAGE_CODE = 'es'

# ─── DETECCIÓN DE ENTORNO ─────────────────────────────────────────────────────
IS_RENDER = os.environ.get('RENDER') is not None

# ─── BASE DE DATOS ─────────────────────────────────────────────────────────────
if IS_RENDER:
    # En Render usa DATABASE_URL de entorno (ya configurado en tu servicio)
    DATABASES = {
        'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
    }
else:
    # Local: tu PostgreSQL local
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql',
            'NAME':     os.getenv('LOCAL_DB_NAME', 'postgres'),
            'USER':     os.getenv('LOCAL_DB_USER', 'postgres'),
            'PASSWORD': os.getenv('LOCAL_DB_PASSWORD', 'felipe98'),
            'HOST':     os.getenv('LOCAL_DB_HOST', 'localhost'),
            'PORT':     os.getenv('LOCAL_DB_PORT', '5432'),
        }
    }

# ─── APLICACIONES Y MIDDLEWARE ─────────────────────────────────────────────────
INSTALLED_APPS = [
    "daphne",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'channels',
    'ckeditor',

    # Tus apps
    'accounts.apps.AccountsConfig',
    'chatbotcito',
    'chat',
    'videollamadas',
    'blogs',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ─── RUTAS, ASGI Y WSGI ────────────────────────────────────────────────────────
ROOT_URLCONF = 'GranGusano.urls'
WSGI_APPLICATION = 'GranGusano.wsgi.application'
ASGI_APPLICATION = 'GranGusano.asgi.application'

# ─── TEMPLATES ─────────────────────────────────────────────────────────────────
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

# ─── ESTÁTICOS Y MEDIA ─────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise para producción en Render
STATICFILES_STORAGE = (
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
    if IS_RENDER else 'django.contrib.staticfiles.storage.StaticFilesStorage'
)

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ─── AUTENTICACIÓN y Allauth ──────────────────────────────────────────────────
AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

SITE_ID = 1
ACCOUNT_FORMS = {'login': 'accounts.forms.CustomLoginForm'}
ACCOUNT_EMAIL_VERIFICATION = "mandatory" if IS_RENDER else "none"
ACCOUNT_EMAIL_REQUIRED     = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_LOGIN_ATTEMPTS_LIMIT   = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300

LOGIN_REDIRECT_URL        = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'
ACCOUNT_SIGNUP_REDIRECT_URL = '/accounts/login/'
LOGIN_URL = '/accounts/login/'

# ─── EMAIL ────────────────────────────────────────────────────────────────────
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST    = 'smtp.gmail.com'
EMAIL_PORT    = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER     = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# ─── VALIDADORES de contraseña ─────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── CHANNEL LAYERS (WebSockets) ──────────────────────────────────────────────
# No cambies REDIS_URL en .env; se usará tal cual tengas configurado.
if IS_RENDER:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [os.getenv('REDIS_URL')],
            },
        },
    }
else:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [os.getenv('REDIS_URL', 'redis://127.0.0.1:6379')],
            },
        },
    }

# ─── JAAS (Videollamadas) ─────────────────────────────────────────────────────
JAAS_APP_ID             = os.getenv("JAAS_APP_ID")
JAAS_TENANT             = os.getenv("JAAS_TENANT")
JAAS_PRIVATE_KEY_PATH   = os.getenv("JAAS_PRIVATE_KEY_PATH")
JAAS_KID                = os.getenv("JAAS_KID")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'