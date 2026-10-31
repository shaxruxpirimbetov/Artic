from pathlib import Path
from decouple import config
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = False
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="").split(",")
AUTH_USER_MODEL = "user.User"

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_APPS = [
    "rest_framework",
    "corsheaders"
]
LOCAL_APPS = [
    "apps.user",
    "apps.art",
    "apps.comment",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_APPS + LOCAL_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Artic.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'Artic.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny"
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle"
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/minute",
        "user": "1000/minute"
    },
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer"
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser"
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    # "ROTATE_REFRESH_TOKENS": False,
    # "BLACKLIST_AFTER_ROTATION": False,
    # "UPDATE_LAST_LOGIN": False,
    #
    "ALGORITHM": "HS256",
    "SIGNING_KEY": config("SECRET_KEY"),
    # "VERIFYING_KEY": "",
    # "AUDIENCE": None,
    # "ISSUER": None,
    # "JSON_ENCODER": None,
    # "JWK_URL": None,
    # "LEEWAY": 0,
    #
    # "AUTH_HEADER_TYPES": ("Bearer",),
    # "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    # "USER_ID_FIELD": "id",
    # "USER_ID_CLAIM": "user_id",
    # "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    #
    # "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    # "TOKEN_TYPE_CLAIM": "token_type",
    # "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    #
    # "JTI_CLAIM": "jti",
    #
    # "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    # "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    # "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    #
    # "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    # "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    # "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    # "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    # "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    # "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
    #
    # "CHECK_REVOKE_TOKEN": False,
    # "REVOKE_TOKEN_CLAIM": "hash_password",
    # "CHECK_USER_IS_ACTIVE": True,
}

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS=True

else:
    CORS_ALLOWED_ORIGINS=config("CORS_ALLOWED_ORIGINS").split(",")

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         "file": {
#             "level": "INFO",
#             "class": "logging.FileHandler",
#             "filename": BASE_DIR / "debug.log"
#         },
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["file"],
#             "level": "INFO",
#             "propagate": True
#         }
#     }
# }


CLOUDFLARE_ACCOUNT_ID = config("CLOUDFLARE_ACCOUNT_ID")

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

AWS_ACCESS_KEY_ID = config("CLOUDFLARE_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("CLOUDFLARE_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = config("CLOUDFLARE_R2_BUCKET")
AWS_S3_ENDPOINT_URL = f"https://{CLOUDFLARE_ACCOUNT_ID}.r2.cloudflarestorage.com"
AWS_S3_CUSTOM_DOMAIN = config("CLOUDFLARE_R2_PUBLIC_URL").replace("https://", "")
AWS_S3_REGION_NAME = "auto"
AWS_DEFAULT_ACL = None
AWS_S3_ADDRESSING_STYLE = "virtual"
AWS_QUERYSTRING_AUTH = False  # чтобы публичные URL были без подписи
