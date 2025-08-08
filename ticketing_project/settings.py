from pathlib import Path
import os # Import the os module

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Smart Settings for Live vs. Local ---
# Check if the code is running on PythonAnywhere
if 'PYTHONANYWHERE_SITE' in os.environ:
    DEBUG = False
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') # Will be set on the server
    ALLOWED_HOSTS = ['yuvrajbhadauriya.pythonanywhere.com']
    CSRF_TRUSTED_ORIGINS = ['https://yuvrajbhadauriya.pythonanywhere.com']
else:
    # Settings for your local computer
    DEBUG = True
    SECRET_KEY = 'django-insecure-a-temporary-secret-key-for-local-dev'
    ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'anymail', # Add anymail
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ticketing_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- Email Configuration ---
if 'PYTHONANYWHERE_SITE' in os.environ:
    # Live settings for Mailgun
    ANYMAIL = {
        "MAILGUN_API_KEY": os.environ.get('MAILGUN_API_KEY'),
        "MAILGUN_SENDER_DOMAIN": os.environ.get('MAILGUN_SENDER_DOMAIN'),
    }
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
    DEFAULT_FROM_EMAIL = "tickets@your_verified_mailgun_domain.com" # Replace with your real domain later
else:
    # Local settings (Gmail or console)
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'yuvraj.tedx@gmail.com'
    EMAIL_HOST_PASSWORD = 'xiiohxweueoggohy'
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# Static and Media files
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
