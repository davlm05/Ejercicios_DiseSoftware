"""URL configuration for the ``localizacion`` bundle.

Used when ``DJANGO_BUNDLE=localizacion``. Exposes only the localización SSR
frontend at the root (``/``).
"""
from django.urls import include, path

urlpatterns = [
    path("", include("apps.localizacion.urls")),
]
