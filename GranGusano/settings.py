from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# ─── BASE Y .env ───────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

# ─── TIMEZONE ──────────────────────────────────────────────────────────────────
TIME_ZONE = 'America/Santiago'
USE_TZ = True
USE_I18N = True
LANGUAGE_CODE = 'es'

# ─── DEBUG Y HOSTS ─────────────────────────────────────────────────────────────
SECRET_KEY = os.getenv('SECRET_KEY', 'clave-dev-insegura')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*']

# ─── DETECCIÓN DE RENDER ──────────────────────────────────────────────────────
IS_RENDER = os.environ.get('RENDER') is not None

# ─── CLOUDINARY (Archivos media) ──────────────────────────────────────────────
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

# ─── JAAS ──────────────────────────────────────────────────────────────────────
JAAS_APP_ID = os.getenv("JAAS_APP_ID")
JAAS_TENANT = os.getenv("JAAS_TENANT")
JAAS_PRIVATE_KEY_PATH = os.getenv("JAAS_PRIVATE_KEY_PATH")
JAAS_KID = os.getenv("JAAS_KID")

# ─── INSTALLED APPS ────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    "daphne",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # Terceros
    'channels',
    'ckeditor',

    # Tus apps
    'accounts.apps.AccountsConfig',
    'chatbotcito',
    'chat',
    'videollamadas',
    'blogs',
]

# ─── MIDDLEWARE ────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← ¡IMPORTANTE!
    'django.contrib.sessions.middleware.SessionMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ─── URLS Y TEMPLATES ──────────────────────────────────────────────────────────
ROOT_URLCONF = 'GranGusano.urls'
WSGI_APPLICATION = 'GranGusano.wsgi.application'
ASGI_APPLICATION = "GranGusano.asgi.application"

TEMPLATES = [
    {
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
    },
]

# ─── BASE DE DATOS ─────────────────────────────────────────────────────────────
if IS_RENDER:
    DATABASES = {
        'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'felipe98',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

# ─── STATIC Y MEDIA ────────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = (
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
    if IS_RENDER else 'django.contrib.staticfiles.storage.StaticFilesStorage'
)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ─── AUTENTICACIÓN ─────────────────────────────────────────────────────────────
AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

SITE_ID = 1

ACCOUNT_FORMS = {
    'login': 'accounts.forms.CustomLoginForm',
}

ACCOUNT_EMAIL_VERIFICATION = "mandatory" if IS_RENDER else "none"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300

LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'
ACCOUNT_SIGNUP_REDIRECT_URL = '/accounts/login/'
LOGIN_URL = '/accounts/login/'

# ─── EMAIL ─────────────────────────────────────────────────────────────────────
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# ─── VALIDADORES DE CONTRASEÑA ────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── REDIS PARA CHANNELS ──────────────────────────────────────────────────────
REDIS_URL = os.getenv('REDIS_URL')

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
        },
    },
}

# ─── AUTO FIELD ───────────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
