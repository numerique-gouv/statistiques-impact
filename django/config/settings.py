"""
Django settings for config project.
"""

import os
from pathlib import Path
import dj_database_url

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.getenv("DEBUG") == "True" else False

ALLOWED_HOSTS = (
    os.getenv("ALLOWED_HOSTS", "127.0.0.1,.localhost").replace(" ", "").split(",")
)


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "revproxy.apps.RevProxyConfig",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "widget_tweaks",
    "dsfr",
    "core",
    "rest_framework",
    "rest_framework_api_key",
    "drf_spectacular",
    "drf_spectacular_sidecar",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "dsfr/templates"),
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "dsfr.context_processors.site_config",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    raise ValueError("Please set the DATABASE_URL environment variable")

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "fr-fr"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

API_KEY_CUSTOM_HEADER = "HTTP_X_API_KEY"
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")

# Setting for revproxy
UPSTREAM_EXPRESS = os.getenv("UPSTREAM_EXPRESS")
ENVIRONMENT = os.getenv("ENVIRONMENT")


# Spectacular settings
SPECTACULAR_SETTINGS = {
    "TITLE": "Statistique d'usage",
    "DESCRIPTION": "API pour les statistiques d'usage des produits de l'OPI",
    "VERSION": "2.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}


USE_THOUSAND_SEPARATOR = True

# DATAGOUV SETTINGS
DATAGOUV_API_URL = os.getenv("DATAGOUV_API_URL", None)
DATAGOUV_API_KEY = os.getenv("DATAGOUV_API_KEY", None)
DATAGOUV_DEMO_API_KEY = os.getenv("DATAGOUV_DEMO_API_KEY", None)

# POSTHOG SETTINGS
POSTHOG_API_URL = os.getenv("POSTHOG_API_URL", "https://eu.posthog.com")
POSTHOG_API_KEY = os.getenv("POSTHOG_API_KEY", None)
