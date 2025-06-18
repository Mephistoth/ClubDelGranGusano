from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

TIME_ZONE = 'America/Santiago'
USE_TZ = True

SECRET_KEY = 'django-insecure-&7*9br49w%0i$k*v=h_92d)=5tdjipxt38k9p)e7s&)p672*@r'
DEBUG = True
ALLOWED_HOSTS = ['*']

JAAS_APP_ID = os.getenv("JAAS_APP_ID")
JAAS_TENANT = os.getenv("JAAS_TENANT")
JAAS_PRIVATE_KEY_PATH = os.getenv("JAAS_PRIVATE_KEY_PATH")
JAAS_KID = os.getenv("JAAS_KID")

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
    'accounts.apps.AccountsConfig',
    'chatbotcito',
    'chat',
    'videollamadas',
    'blogs',
    'ckeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Agregado para servir estáticos en producción
    'django.contrib.sessions.middleware.SessionMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'GranGusano.urls'

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

WSGI_APPLICATION = 'GranGusano.wsgi.application'
ASGI_APPLICATION = "GranGusano.asgi.application"

IS_RENDER = os.environ.get('RENDER') is not None

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

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

LANGUAGE_CODE = 'es'
USE_I18N = True

# Configuración archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Necesario para collectstatic en Render
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # WhiteNoise

# Archivos media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1

ACCOUNT_FORMS = {
    'login': 'accounts.forms.CustomLoginForm',
}

ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300

LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'
ACCOUNT_SIGNUP_REDIRECT_URL = '/accounts/login/'
LOGIN_URL = '/accounts/login/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}
