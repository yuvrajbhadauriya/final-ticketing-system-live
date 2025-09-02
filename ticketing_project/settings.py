from pathlib import Path
import os

# --- CORE SETTINGS ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY WARNING ---
# This file reads secrets from environment variables.
# On a free PythonAnywhere account, you must manually edit these
# values directly on the server. Do not commit your real secrets to GitHub.

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'a-default-secret-key-for-local-use-only')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# --- HOSTS CONFIGURATION ---
ALLOWED_HOSTS = [
    'yuvrajbhadauriya.pythonanywhere.com',
    'tedxvips2025tickets.pythonanywhere.com',
    'passes.tedxvips.com',
    'www.passes.tedxvips.com',
]
if DEBUG:
    ALLOWED_HOSTS.extend(['127.0.0.1', 'localhost'])

CSRF_TRUSTED_ORIGINS = [
    'https://yuvrajbhadauriya.pythonanywhere.com',
    'https://tedxvips2025tickets.pythonanywhere.com',
    'https://passes.tedxvips.com',
    'https://www.passes.tedxvips.com',
]
if DEBUG:
    CSRF_TRUSTED_ORIGINS.append('http://127.0.0.1:8000')

# --- APP CONFIGURATION ---
INSTALLED_APPS = ['django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', 'import_export', 'anymail', 'tickets']
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF = 'ticketing_project.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.debug', 'django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION = 'ticketing_project.wsgi.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}
AUTH_PASSWORD_VALIDATORS = [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}, {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}, {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}, {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}]
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles_build'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- EMAIL CONFIGURATION ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'tedxvips.tickets@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'tktdyntdzztllxsv')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

