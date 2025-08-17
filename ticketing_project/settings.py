from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Reads the secret key from an environment variable on the server
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'a-default-secret-key-for-local-use')

# Production settings
DEBUG = False
ALLOWED_HOSTS = ['yuvrajbhadauriya.pythonanywhere.com']
CSRF_TRUSTED_ORIGINS = ['https://yuvrajbhadauriya.pythonanywhere.com']

INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    'import_export','anymail', 'tickets',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ticketing_project.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.debug', 'django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION = 'ticketing_project.wsgi.application'

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}


# --- NEW: Email Settings for Gmail ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tedxvips.tickets@gmail.com'  # <-- REPLACE THIS with your full Gmail address
EMAIL_HOST_PASSWORD = 'rimukobgqvntqzfl' # This is your App Password (spaces removed)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles_build'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Other settings
AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
