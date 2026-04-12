"""URL configuration for the ``invitados`` bundle.

Used when ``DJANGO_BUNDLE=invitados``. Exposes only the invitados SSR frontend
at the root (``/``), so it works as a standalone app on its own port.
"""
from django.urls import include, path

urlpatterns = [
    path("", include("apps.invitados.urls")),
]
