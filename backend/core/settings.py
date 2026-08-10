"""
Django settings for AI-Powered Code Review Platform
"""

import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
import dj_database_url  # You'll need to install this

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-8x7y9z1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z')
ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1', 'ai-code-review-platform-79dq.onrender.com','.onrender.com',  # This allows all Render subdomains
    '*', ]
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
    'django_filters',
    'guardian',
    
    # Local apps
    'home',
    'accounts',
    'code_review',
    'dashboard',
    #'ai_analysis',
    'reports',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'ai_code_review_db'),
        'USER': os.getenv('DB_USER', 'Abi'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'Abi17102004'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5433'),
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Authentication backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
    },
}

# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.getenv('ACCESS_TOKEN_LIFETIME', 15))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.getenv('REFRESH_TOKEN_LIFETIME', 7))),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': os.getenv('JWT_SECRET_KEY', SECRET_KEY),
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# CORS Configuration - Complete
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_EXPOSE_HEADERS = [
    'content-type',
    'x-csrftoken',
]

# For development only - allows all origins
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ORIGIN_ALLOW_ALL = True

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE = int(os.getenv('MAX_UPLOAD_SIZE', 10485760))
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760
ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS', '.py,.js,.java,.cpp,.c,.html,.css,.go,.rs,.rb,.php,.cs,.ts,.jsx,.tsx').split(',')

# Security Settings (Production)
if not DEBUG:
    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False') == 'True'
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False') == 'True'
    CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'False') == 'True'
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# Create logs directory if it doesn't exist
os.makedirs(BASE_DIR / 'logs', exist_ok=True)

# Email Configuration
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# AI Configuration
AI_PROVIDER = os.getenv('AI_PROVIDER', 'gemini')  # Changed to 'gemini' as default
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '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')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AQ.Ab8RN6JgZAPeo2MiwXli4dLikND_weaCCfGX7ourtYF-zN7qsg')
AI_MODEL = os.getenv('AI_MODEL', 'gpt-4-turbo-preview')
AI_TEMPERATURE = float(os.getenv('AI_TEMPERATURE', 0.7))
AI_MAX_TOKENS = int(os.getenv('AI_MAX_TOKENS', 2000))

# GitHub Integration (Optional)
GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID', '')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET', '')
GITHUB_REDIRECT_URI = os.getenv('GITHUB_REDIRECT_URI', '')

# Report Settings
REPORT_STORAGE_PATH = BASE_DIR / 'reports'
os.makedirs(REPORT_STORAGE_PATH, exist_ok=True)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AQ.Ab8RN6JgZAPeo2MiwXli4dLikND_weaCCfGX7ourtYF-zN7qsg')

print(f"GEMINI_API_KEY loaded: {bool(GEMINI_API_KEY)}")