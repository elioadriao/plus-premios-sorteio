from pathlib import Path

from decouple import config

import os

import dj_database_url


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

SECRET_KEY = config(
    "RAFFLE_SECRET_KEY",
    default="!cnpua@t(9ozdnq@rre^+21p*c%)s#w@dk+8(r7*!9kp*)sey-"
)


DEBUG = config(
    "RAFFLE_DEBUG",
    cast=bool,
    default=True
)

WHATSAPP_LINK = config(
    "RAFFLE_WHATSAPP_LINK",
    default="https://api.whatsapp.com/send?phone=558281196143&text=Pagamento%20no%20Valor%20R$%20{},00"
)

ALLOWED_HOSTS = config(
    "RAFFLE_ALLOWED_HOSTS",
    default="*",
    cast=lambda v: [s.strip() for s in v.split(",")]
)


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sortition.account",
    "sortition.raffle",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "sortition.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "sortition/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "sortition.wsgi.application"


# Database

DATABASES = {
    "default": dj_database_url.config(
        default=config(
            "RAFFLE_DATABASE",
            default="sqlite:///db.sqlite3"
        )
    )
}


# Password validation

AUTH_USER_MODEL = "account.User"

LOGIN_URL = "/account/add/"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
]


# Internationalization

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Media files

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
