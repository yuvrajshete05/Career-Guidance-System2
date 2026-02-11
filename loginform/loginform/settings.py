

import os
from pathlib import Path
from decouple import config
import dj_database_url




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
    'channels', 
    'djangochannelsrestframework',
    
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


ROOT_URLCONF = 'loginform.urls'
WSGI_APPLICATION = 'loginform.wsgi.application'

ASGI_APPLICATION = 'loginform.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)], # This should be pointing to your WSL Redis
        },
    },
}

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'

GEMINI_API_KEY = "AIzaSyAklf_S-axbIpeNE1dIj1T4un31giE__fU"

JOB_API_KEY = "333797cb571b25e8fb0ac52eecb757f0"


















# import os
# from pathlib import Path

# # ----------------------------------------------------------------------
# # Base directory
# # ----------------------------------------------------------------------
# BASE_DIR = Path(__file__).resolve().parent.parent

# # ----------------------------------------------------------------------
# # Security settings
# # ----------------------------------------------------------------------
# SECRET_KEY = 'django-insecure-your-default-key-for-dev-only'
# DEBUG = True
# ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'career-guidance-system-2.onrender.com', 'career-guidance-system-1-rn6b.onrender.com']

# # ----------------------------------------------------------------------
# # Deployment settings
# # ----------------------------------------------------------------------
# PORT = os.environ.get('PORT', '8000')
# CSRF_TRUSTED_ORIGINS = [
#     "https://career-guidance-system-2.onrender.com",
#     "https://career-guidance-system-1-rn6b.onrender.com",
#     "http://127.0.0.1:8000",
#     "http://localhost:8000",
# ]
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# # ----------------------------------------------------------------------
# # Application definition
# # ----------------------------------------------------------------------
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'app1',
#     'loginform',
#     'channels', 
#     'djangochannelsrestframework',
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

# ROOT_URLCONF = 'loginform.urls'
# WSGI_APPLICATION = 'loginform.wsgi.application'
# ASGI_APPLICATION = 'loginform.asgi.application'

# # ----------------------------------------------------------------------
# # Channels / Redis configuration
# # ----------------------------------------------------------------------
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [('127.0.0.1', 6379)],
#         },
#     },
# }

# # ----------------------------------------------------------------------
# # Templates
# # ----------------------------------------------------------------------
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

# # ----------------------------------------------------------------------
# # Database - Supabase PostgreSQL
# # ----------------------------------------------------------------------
# # DATABASES = {
# #     'default': {
# #         'ENGINE': 'django.db.backends.postgresql',
# #         'NAME': 'postgres',
# #         'USER': 'postgres',
# #         'PASSWORD': 'FOdm1G3h9gG6hKvv',
# #         'HOST': '2406:da1a:6b0:f600:ab4f:9501:889f:a547',
# #         'PORT': '5432',
# #     }
# # }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'PASSWORD': 'FOdm1G3h9gG6hKvv',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#         'OPTIONS': {
#             'sslmode': 'require',  # Supabase requires SSL
#         },
#     }
# }


# # import os
# # from pathlib import Path
# # from decouple import config
# # import dj_database_url

# # DATABASES = {
# #     'default': dj_database_url.parse(config('DATABASE_URL', default=f'sqlite:///{BASE_DIR / "db.sqlite3"}'))
# # }




# # ----------------------------------------------------------------------
# # Password validation
# # ----------------------------------------------------------------------
# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# ]

# # ----------------------------------------------------------------------
# # Localization
# # ----------------------------------------------------------------------
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True

# # ----------------------------------------------------------------------
# # Static files
# # ----------------------------------------------------------------------
# STATIC_URL = 'static/'

# # ----------------------------------------------------------------------
# # Default primary key field type
# # ----------------------------------------------------------------------
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # ----------------------------------------------------------------------
# # Login redirect
# # ----------------------------------------------------------------------
# LOGIN_REDIRECT_URL = '/'

# # ----------------------------------------------------------------------
# # API Keys
# # ----------------------------------------------------------------------
# GEMINI_API_KEY = "AIzaSyAWKyx5YW-bbgUkwi6rjohVvq3lzTc8k-w"
# JOB_API_KEY = "333797cb571b25e8fb0ac52eecb757f0"


































# import os
# from pathlib import Path
# from decouple import config
# import dj_database_url

# BASE_DIR = Path(__file__).resolve().parent.parent

# # ----------------------------------------------------------------------
# # Security settings
# # ----------------------------------------------------------------------
# SECRET_KEY = config('DJANGO_SECRET_KEY', default='django-insecure-your-default-key-for-dev-only')
# DEBUG = config('DEBUG', default=True, cast=bool)
# ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')

# # ----------------------------------------------------------------------
# # Deployment-specific settings
# # ----------------------------------------------------------------------
# PORT = os.environ.get('PORT', '8000')
# CSRF_TRUSTED_ORIGINS = [
#     "https://career-guidance-system-2.onrender.com",
#     "https://career-guidance-system-1-rn6b.onrender.com",
#     "http://127.0.0.1:8000",
#     "http://localhost:8000",
# ]
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# # ----------------------------------------------------------------------
# # Application definition
# # ----------------------------------------------------------------------
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',

#     # Your apps
#     'app1',
#     'loginform',

#     # Third party
#     'channels',
#     'djangochannelsrestframework',
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

# ROOT_URLCONF = 'loginform.urls'
# WSGI_APPLICATION = 'loginform.wsgi.application'
# ASGI_APPLICATION = 'loginform.asgi.application'

# # ----------------------------------------------------------------------
# # Channels / Redis
# # ----------------------------------------------------------------------
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [("127.0.0.1", 6379)],  # Change if using Docker/Render Redis
#         },
#     },
# }

# # ----------------------------------------------------------------------
# # Templates
# # ----------------------------------------------------------------------
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

# # ----------------------------------------------------------------------
# # Database
# # ----------------------------------------------------------------------
# # Use DATABASE_URL if present, otherwise fallback to SQLite
# DATABASES = {
#     'default': dj_database_url.config(
#         default="postgresql://postgres:FOdm1G3h9gG6hKvv@db.vtxsrgydlmxticzismle.supabase.co:5432/postgres",
#         conn_max_age=600,
#         ssl_require=True
#     )
# }


# # ----------------------------------------------------------------------
# # Passwords
# # ----------------------------------------------------------------------
# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# ]

# # ----------------------------------------------------------------------
# # Localization
# # ----------------------------------------------------------------------
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True

# # ----------------------------------------------------------------------
# # Static files
# # ----------------------------------------------------------------------
# STATIC_URL = 'static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles'

# # ----------------------------------------------------------------------
# # Misc
# # ----------------------------------------------------------------------
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# LOGIN_REDIRECT_URL = '/'

# # ----------------------------------------------------------------------
# # API Keys
# # ----------------------------------------------------------------------
# GEMINI_API_KEY = config("GEMINI_API_KEY", default="")
# JOB_API_KEY = config("JOB_API_KEY", default="")

