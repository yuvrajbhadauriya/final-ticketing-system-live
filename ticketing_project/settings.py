from pathlib import Path
import os

# --- CORE SETTINGS ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY ENHANCEMENT 1: DEVELOPMENT MODE TOGGLE ---
# This is the most important setting for security.
# It defaults to False (production mode).
# Set the DEVELOPMENT_MODE environment variable to "True" on your local machine only.
DEVELOPMENT_MODE = os.environ.get('DEVELOPMENT_MODE', 'False').lower() == 'true'

# --- SECURITY ENHANCEMENT 2: SECRET KEY MANAGEMENT ---
# The secret key is read from an environment variable on the server.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'a-default-secret-key-for-local-use-only')

# --- DEBUG SETTING ---
# DEBUG is now safely controlled by DEVELOPMENT_MODE.
DEBUG = DEVELOPMENT_MODE

# --- ALLOWED HOSTS ---
# Defines which domains can access your site.
if DEVELOPMENT_MODE:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
else:
    # Add your live domain(s) here.
    ALLOWED_HOSTS = [
        'yuvrajbhadauriya.pythonanywhere.com',
        'tedxvips2025tickets.pythonanywhere.com',
        'passes.tedxvips.com',
        'www.passes.tedxvips.com'
    ]

# --- CSRF PROTECTION ---
CSRF_TRUSTED_ORIGINS = [
    'https://yuvrajbhadauriya.pythonanywhere.com',
    'https://tedxvips2025tickets.pythonanywhere.com',
    'https://passes.tedxvips.com',
    'https://www.passes.tedxvips.com'
]
# Add local servers to trusted origins only in development mode
if DEVELOPMENT_MODE:
    CSRF_TRUSTED_ORIGINS.extend([
        'http://127.0.0.1:8000',
        'http://localhost:8000',
    ])


# --- INSTALLED APPS ---
INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    'import_export','anymail', 'tickets',
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- URLS, TEMPLATES, WSGI ---
ROOT_URLCONF = 'ticketing_project.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.debug', 'django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION = 'ticketing_project.wsgi.application'

# --- DATABASE ---
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}

# --- EMAIL SETTINGS ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

if DEVELOPMENT_MODE:
    # For local testing, you can add credentials here.
    EMAIL_HOST_USER = 'tedxvips.tickets@gmail.com'
    EMAIL_HOST_PASSWORD = 'tktdyntdzztllxsv'
else:
    # In production, credentials are read from secure environment variables.
    EMAIL_HOST_USER = os.environ.get('tedxvips.tickets@gmail.com')
    EMAIL_HOST_PASSWORD = os.environ.get('tktdyntdzztllxsv')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# --- PASSWORD VALIDATION ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internationalization & Static/Media Files ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles_build'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- PRODUCTION SECURITY HEADERS ---
# These settings are only active when DEBUG is False.
if not DEVELOPMENT_MODE:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000 # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

