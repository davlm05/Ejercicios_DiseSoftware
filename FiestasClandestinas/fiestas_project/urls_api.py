"""URL configuration for the ``api`` bundle.

Used when ``DJANGO_BUNDLE=api``. Exposes only the REST endpoints.
"""
from django.http import JsonResponse
from django.urls import include, path


def index(request):
    return JsonResponse({"bundle": "api", "status": "ok"})


urlpatterns = [
    path("", index),
    path("api/", include("apps.api.urls")),
]
