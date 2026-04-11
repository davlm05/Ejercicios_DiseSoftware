"""Django settings for the Fiestas Clandestinas monolith.

This project is a monolith but is designed to run as separate *bundles*.
The bundle is selected with the ``DJANGO_BUNDLE`` environment variable:

- ``all``          → full monolith (default)
- ``api``          → only the REST API
- ``invitados``    → only the SSR frontend for invitados
- ``localizacion`` → only the SSR frontend for localización

The actual URL routing for each bundle lives in ``feature/bundles-scripts``.
At ``feature/backend-core`` the variable is read and stored in
``settings.BUNDLE`` but all bundles share the same ``ROOT_URLCONF``.
"""
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security --------------------------------------------------------------
# Local-only academic project, so the key is hard-coded. Rotate if the repo
# ever becomes public.
SECRET_KEY = "django-insecure-fiestas-clandestinas-local-dev-key"
DEBUG = True
ALLOWED_HOSTS = ["*"]

# --- Bundle switch ---------------------------------------------------------
BUNDLE = os.environ.get("DJANGO_BUNDLE", "all")

# --- Applications ----------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Local apps
    "fiestas_core",
    "apps.api.apps.ApiConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "fiestas_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "fiestas_project.wsgi.application"

# --- Database --------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --- Password validation ---------------------------------------------------
AUTH_PASSWORD_VALIDATORS = []

# --- Internationalization --------------------------------------------------
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Costa_Rica"
USE_I18N = True
USE_TZ = True

# --- Static files ----------------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
