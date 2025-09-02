from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY ENHANCEMENT 1: DEVELOPMENT vs PRODUCTION ---
# This variable controls whether the application runs in debug or production mode.
# FIX: Default to 'True' for local development.
DEVELOPMENT_MODE = os.environ.get('DEVELOPMENT_MODE', 'True') == 'True'

# --- Set DEBUG based on the development mode ---
DEBUG = DEVELOPMENT_MODE

# --- Define ALLOWED_HOSTS for production and development ---
# In production, only your live domains are allowed.
ALLOWED_HOSTS = [
    'yuvrajbhadauriya.pythonanywhere.com',
    'tedxvips2025tickets.pythonanywhere.com',
    'passes.tedxvips.com',
    'www.passes.tedxvips.com',
]

# In development mode, we add local addresses for testing.
if DEVELOPMENT_MODE:
    ALLOWED_HOSTS.extend([
        '127.0.0.1',
        'localhost',
    ])

# --- SECURITY ENHANCEMENT 2: SECRET KEY ---
# The secret key is safely read from an environment variable.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-local-default-key-change-me')

CSRF_TRUSTED_ORIGINS = [
    'https://yuvrajbhadauriya.pythonanywhere.com',
    'https://tedxvips2025tickets.pythonanywhere.com',
    'https://passes.tedxvips.com',
    'https://www.passes.tedxvips.com'
]

# Add local development servers to trusted origins in development mode
if DEVELOPMENT_MODE:
    CSRF_TRUSTED_ORIGINS.extend([
        'http://127.0.0.1:8000',
        'http://localhost:8000',
    ])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export',
    'anymail',
    'tickets',
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

# Database
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}

# --- SECURITY ENHANCEMENT 3: SECURE EMAIL SETTINGS ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# --- FIX FOR LOCAL TESTING ---
if DEVELOPMENT_MODE:
    # For local testing, temporarily add your credentials here.
    # IMPORTANT: DO NOT deploy this version to your live server.
    EMAIL_HOST_USER = 'tedxvips.tickets@gmail.com'  # <-- Your full Gmail address
    EMAIL_HOST_PASSWORD = 'tktdyntdzztllxsv' # <-- Your Gmail App Password
else:
    # In production, credentials will be read from environment variables.
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
    
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# --- SECURITY ENHANCEMENT 4: PASSWORD VALIDATION ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- SECURITY ENHANCEMENT 5: PRODUCTION-ONLY SECURITY SETTINGS ---
if not DEVELOPMENT_MODE:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000 # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True


