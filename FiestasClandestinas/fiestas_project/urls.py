"""Root URL configuration for the full monolith.

This is the default entry point when ``DJANGO_BUNDLE`` is unset or set to
``all``. It mounts:

- ``/api/`` → REST endpoints (``apps.api``)
- ``/admin/`` → Django admin

The SSR frontends (``apps.invitados`` and ``apps.localizacion``) will be
mounted here in their respective feature branches.
"""
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def index(request):
    return JsonResponse(
        {
            "project": "Fiestas Clandestinas",
            "bundle": "all",
            "status": "ok",
            "endpoints": {
                "GET /api/fiestas": "list available fiestas",
                "POST /api/fiestas": "create a new fiesta",
                "POST /api/invitados/<id>/aceptar": "accept invitation",
                "POST /api/invitados/<id>/rechazar": "decline invitation",
            },
        }
    )


urlpatterns = [
    path("", index, name="index"),
    path("api/", include("apps.api.urls")),
    path("admin/", admin.site.urls),
]
