"""
Django settings for DHV4_Web project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import sys
from pathlib import Path

from django.utils.translation import gettext_lazy as _

from django.db.models import BigAutoField
from django_jinja.builtins import DEFAULT_EXTENSIONS

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "True") != "False"

if DEBUG:
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'u-3sierkapz7b9fp0o82qyulnstk6c8s*8myzw&=*$u@fi4^%%'
else:
    SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = [
    "127.0.0.1",
    os.environ.get("DOMAIN", "localhost")
]

CSRF_TRUSTED_ORIGINS = ["https://" + host for host in ALLOWED_HOSTS]

SITE_ID = 1

if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    CONN_MAX_AGE = None
else:
    INTERNAL_IPS = ALLOWED_HOSTS

# Application definition

INSTALLED_APPS = [
    # https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#overriding-the-default-admin-site
    'DHV4_Web.apps.DHAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'xff.middleware.XForwardedForMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'public.middleware.LogMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    INSTALLED_APPS.append('debug_toolbar')

INSTALLED_APPS.extend(['django.contrib.sites',
                       'django.contrib.sitemaps',
                       'public.apps.PublicConfig',
                       'docs.apps.DocsConfig',
                       'botdata.apps.BotdataConfig',
                       'tags.apps.TagsConfig',
                       'shop.apps.ShopConfig',
                       'stats.apps.StatsConfig',
                       'django_jinja',
                       'django_extensions',
                       'dynamic_raw_id',
                       'imagekit',
                       ])

ROOT_URLCONF = 'DHV4_Web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            "match_extension": ".jinja2",
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            "constants": {
                "canonical_domain_uri": "https://" + os.environ.get("DOMAIN", "duckhunt.me"),
            },
            "extensions": DEFAULT_EXTENSIONS
        },
    },
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

WSGI_APPLICATION = 'DHV4_Web.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("DB_NAME", "duckhunt"),
        'USER': os.environ.get("DB_USER", "duckhunt"),
        'PASSWORD': os.environ.get("DB_PASSWORD", "duckhunt"),
        'HOST': os.environ.get("DB_HOST", "localhost"),
        'PORT': os.environ.get("DB_PORT", "5432"),
    }
}

CONN_MAX_AGE = None

# Cache
# https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-CACHES
if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
            'LOCATION': os.environ.get("MEMCACHED_LOC", "localhost:11211"),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_THOUSAND_SEPARATOR = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.parent.parent / "static"

MEDIA_URL = "/images/"
MEDIA_ROOT = BASE_DIR.parent.parent / "images"

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

DH_API_KEY = os.environ.get("DH_API_KEY", "")
DH_API_URL = os.environ.get("DH_API_URL", "http://duckhunt.me/api")

if not DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "()": "colorlog.ColoredFormatter",
                "format": "{log_color}{levelname}\t {asctime}\t [{name}]{reset} {message}",
                "style": "{",
            },
            "simple": {
                "format": "{levelname} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
            "mail_admins": {
                "level": "ERROR",
                # "class": "django.utils.log.AdminEmailHandler",
                "class": "logging.NullHandler",
                # "include_html": True,
            },
        },
        "root": {
            "handlers": ["console", "mail_admins"],
            "level": "DEBUG",
        },
        "loggers": {
            "django": {
                "handlers": ["console", "mail_admins"],
                "level": "INFO",
                "propagate": False,
            },
            "discord": {
                "handlers": ["console", "mail_admins"],
                "level": "INFO",
                "propagate": False,
            },
            "asyncio": {
                "handlers": ["console", "mail_admins"],
                "level": "INFO",
                "propagate": False,
            },
            "parso.*": {
                "handlers": ["console", "mail_admins"],
                "level": "INFO",
                "propagate": False,
            },
            "paramiko.transport": {
                "handlers": ["console", "mail_admins"],
                "level": "INFO",
                "propagate": False,
            },
            "urllib3.connectionpool": {
                "handlers": ["console", "mail_admins"],
                "level": "INFO",
                "propagate": False,
            },
            "PIL.*": {
                "handlers": ["console", "mail_admins"],
                "level": "INFO",
                "propagate": False,
            },
            "MARKDOWN": {
                "handlers": ["console", "mail_admins"],
                "level": "INFO",
                "propagate": False,
            },
            "parso.python.diff": {
                "handlers": ["console", "mail_admins"],
                "level": "INFO",
                "propagate": False,
            },
            "fontTools": {
                "handlers": ["console", "mail_admins"],
                "level": "INFO",
                "propagate": False,
            },
            "fontTools.subset": {
                "handlers": ["console", "mail_admins"],
                "level": "WARNING",
                "propagate": False,
            },
        },
    }

    print("XFF")

    XFF_TRUSTED_PROXY_DEPTH = 1
    XFF_STRICT = False

    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )  # https://caddyserver.com/docs/caddyfile/directives/reverse_proxy#headers

IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = 'imagekit.cachefiles.strategies.Optimistic'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LANGUAGES = [
    ("en", _("English")),
    ("fr", _("French")),
]

LOCALE_PATHS = [
    BASE_DIR / "locales"
]
