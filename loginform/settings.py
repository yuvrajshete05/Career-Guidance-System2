# import os
# from pathlib import Path
# from decouple import config
# import dj_database_url

# # ------------------------------------------------------------------------------
# # Base directory
# # ------------------------------------------------------------------------------
# BASE_DIR = Path(__file__).resolve().parent.parent

# # ------------------------------------------------------------------------------
# # Security settings
# # ------------------------------------------------------------------------------
# SECRET_KEY = config('DJANGO_SECRET_KEY', default='django-insecure-your-default-key-for-dev-only')
# DEBUG = config('DEBUG', default=True, cast=bool)
# ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')

# # ------------------------------------------------------------------------------
# # Deployment-specific settings
# # ------------------------------------------------------------------------------
# PORT = os.environ.get('PORT', '8000')
# CSRF_TRUSTED_ORIGINS = [
#     "https://career-guidance-system-2.onrender.com",
#     "https://career-guidance-system-1-rn6b.onrender.com",
# ]
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# # ------------------------------------------------------------------------------
# # Application definition
# # ------------------------------------------------------------------------------
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'app1',
#     'loginform',
#     'channels'
#     # Removed 'career' because the app folder doesn't exist
#     # 'career',
# ]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# # ------------------------------------------------------------------------------
# # URLs and WSGI application
# # Set ROOT_URLCONF to your main project's urls.py, which is 'loginform.urls'
# # based on your directory structure.
# # ------------------------------------------------------------------------------
# ROOT_URLCONF = 'loginform.urls' # Corrected based on your project structure
# WSGI_APPLICATION = 'loginform.wsgi.application'

# # ------------------------------------------------------------------------------
# # Templates
# # ------------------------------------------------------------------------------
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [BASE_DIR / 'templates'],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# # ------------------------------------------------------------------------------
# # Database configuration
# # ------------------------------------------------------------------------------
# if config('DATABASE_URL', default=''):
#     DATABASES = {
#         'default': dj_database_url.parse(config('DATABASE_URL'))
#     }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': config('DB_ENGINE', default='django.db.backends.postgresql'),
#             'NAME': config('DB_NAME', default='career_db'),
#             'USER': config('DB_USER', default='yuvraj05'),
#             'PASSWORD': config('DB_PASSWORD', default='yuvraj'),
#             'HOST': config('DB_HOST', default='127.0.0.1'),
#             'PORT': config('DB_PORT', default='5432', cast=int),
#         }
#     }
#     if DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql' and not config('DB_NAME', default=''):
#         DATABASES = {
#             'default': {
#                 'ENGINE': 'django.db.backends.sqlite3',
#                 'NAME': BASE_DIR / 'db.sqlite3',
#             }
#         }

# # ------------------------------------------------------------------------------
# # Password validation
# # ------------------------------------------------------------------------------
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

# # ------------------------------------------------------------------------------
# # Internationalization
# # ------------------------------------------------------------------------------
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True

# # ------------------------------------------------------------------------------
# # Static files (CSS, JS, Images)
# # ------------------------------------------------------------------------------
# STATIC_URL = 'static/'

# # ------------------------------------------------------------------------------
# # Default primary key field type
# # ------------------------------------------------------------------------------
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # ------------------------------------------------------------------------------
# # Login redirection URL
# # ------------------------------------------------------------------------------
# LOGIN_REDIRECT_URL = '/'

# # ------------------------------------------------------------------------------
# # Gemini API Key
# # ------------------------------------------------------------------------------
# GEMINI_API_KEY = "AIzaSyAWKyx5YW-bbgUkwi6rjohVvq3lzTc8k-w"






# C:\loginform\settings.py

import os
from pathlib import Path
from decouple import config
import dj_database_url

# ------------------------------------------------------------------------------
# Base directory
# ------------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------------------
# Security settings
# ------------------------------------------------------------------------------
SECRET_KEY = config('DJANGO_SECRET_KEY', default='django-insecure-your-default-key-for-dev-only')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')

# ------------------------------------------------------------------------------
# Deployment-specific settings
# ------------------------------------------------------------------------------
PORT = os.environ.get('PORT', '8000')
CSRF_TRUSTED_ORIGINS = [
    "https://career-guidance-system-2.onrender.com",
    "https://career-guidance-system-1-rn6b.onrender.com",
    # Add your local development origins if needed for testing CSRF,
    # though usually not an issue for WebSockets on 127.0.0.1
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ------------------------------------------------------------------------------
# Application definition
# ------------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app1',
    'loginform',
    'channels' # This line is correct and should be present
    # Removed 'career' because the app folder doesn't exist
    # 'career',
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

# ------------------------------------------------------------------------------
# URLs and WSGI/ASGI applications
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'loginform.urls'
WSGI_APPLICATION = 'loginform.wsgi.application'

# !!! IMPORTANT: CHANNELS ASGI APPLICATION SETTING !!!
# This tells Daphne where to find your main ASGI application for WebSockets.
ASGI_APPLICATION = 'loginform.asgi.application'

# ------------------------------------------------------------------------------
# Channels Layer Configuration (for Redis)
# !!! IMPORTANT: CHANNEL LAYERS SETTING !!!
# This configures Django Channels to use Redis as its backend for real-time communication.
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)], # This should be pointing to your WSL Redis
        },
    },
}

# ------------------------------------------------------------------------------
# Templates
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# ------------------------------------------------------------------------------
# Database configuration
# ------------------------------------------------------------------------------
if config('DATABASE_URL', default=''):
    DATABASES = {
        'default': dj_database_url.parse(config('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': config('DB_ENGINE', default='django.db.backends.postgresql'),
            'NAME': config('DB_NAME', default='career_db'),
            'USER': config('DB_USER', default='yuvraj05'),
            'PASSWORD': config('DB_PASSWORD', default='yuvraj'),
            'HOST': config('DB_HOST', default='127.0.0.1'),
            'PORT': config('DB_PORT', default='5432', cast=int),
        }
    }
    if DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql' and not config('DB_NAME', default=''):
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }

# ------------------------------------------------------------------------------
# Password validation
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ------------------------------------------------------------------------------
# Internationalization
# ------------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------------------
# Static files (CSS, JS, Images)
# ------------------------------------------------------------------------------
STATIC_URL = 'static/'

# ------------------------------------------------------------------------------
# Default primary key field type
# ------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------------------------------------------------------------
# Login redirection URL
# ------------------------------------------------------------------------------
LOGIN_REDIRECT_URL = '/'

# ------------------------------------------------------------------------------
# Gemini API Key
# ------------------------------------------------------------------------------
GEMINI_API_KEY = "AIzaSyAWKyx5YW-bbgUkwi6rjohVvq3lzTc8k-w"


