from pathlib import Path
from datetime import timedelta
from datetime import datetime
import os
from core.utils.logger.middleware import IPLogMiddleware
from core.utils.logger.logging_formatter import SafeFormatter
BASE_DIR = Path(__file__).resolve().parent.parent

# Build paths inside the project like this: BASE_DIR / 'subdir'.



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-g$fx03wp&9@dqiix)8@-c5x2rai=g$c$=5$e$*f!f4=6v83bf5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
PRODUCTION = False if os.getenv("PRODUCTION") == 'False' else True

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_WHITELIST = [
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:5173",
]

# CSRF_TRUSTED_ORIGINS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'customer',
    'property',
    'support',
    'notifications',
 
]

MIDDLEWARE = [
    'core.utils.logger.middleware.IPLogMiddleware',
    'property.middleware.SimpleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'phindr_db',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '3306', 
        }
    }



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'customer.User'

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static",]
STATIC_ROOT = BASE_DIR / 'staticfiles'
IMAGE_PATH =  BASE_DIR / 'static'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'EXCEPTION_HANDLER':
        'core.utils.exceptions.custom_exception_handler',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/m',  # for anonymous users
        'user': '10/m',  # for authenticated users
    }
    
}



SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_PORT = 465
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# Create logs directory if it doesn't exist    :start
LOGS_DIR = os.path.join(BASE_DIR, 'logs')         
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    
    'filters': {
    'add_ip': {
        '()': 'core.utils.logger.logging_filter.RequestIPFilter',
        },
    },
    
    'formatters': {
        'verbose': {
            '()': 'core.utils.logger.logging_formatter.SafeFormatter',
            'format': '{levelname} {asctime} {module} {ip} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            '()': 'core.utils.logger.logging_formatter.SafeFormatter',
            'format': '{levelname} {asctime} {ip} {message}',
            'style': '{',
        },
    
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ['add_ip'],
          
        },
        'daily_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, f'django_{datetime.now().strftime("%Y-%m-%d")}.log'),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 30,  # Keep 30 days of logs
            'formatter': 'verbose',
            'encoding': 'utf-8',
            'filters': ['add_ip'],
           
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, f'error_{datetime.now().strftime("%Y-%m-%d")}.log'),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 30,
            'formatter': 'verbose',
            'encoding': 'utf-8',
            'filters': ['add_ip'],
           
        },
        'database_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, f'database_{datetime.now().strftime("%Y-%m-%d")}.log'),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 15,
            'formatter': 'verbose',
            'encoding': 'utf-8',
            'filters': ['add_ip'],
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'daily_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['database_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # Your app logger
        'core': {  # Replace with your actual app name
            'handlers': ['console', 'daily_file', 'error_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # Root logger
        '': {
            'handlers': ['console', 'daily_file'],
            'level': 'INFO',
        }
    }
}
# :END

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
