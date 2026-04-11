"""Root URL configuration for the full monolith.

This is the default entry point when ``DJANGO_BUNDLE`` is unset or set to
``all``. At ``feature/backend-core`` it only exposes the Django admin and a
trivial index view. The real URLs for the API and the two SSR frontends are
added in later feature branches (``feature/api-fiestas``,
``feature/frontend-invitados``, ``feature/frontend-localizacion``).
"""
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path


def index(request):
    return JsonResponse(
        {
            "project": "Fiestas Clandestinas",
            "bundle": "all",
            "status": "ok",
            "hint": "endpoints will be mounted in later feature branches",
        }
    )


urlpatterns = [
    path("", index, name="index"),
    path("admin/", admin.site.urls),
]
