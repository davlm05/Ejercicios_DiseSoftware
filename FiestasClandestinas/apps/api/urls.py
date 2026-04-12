"""URL patterns for the REST API.

Mounted under ``/api/`` by ``fiestas_project.urls``.
"""
from django.urls import path

from apps.api import views

app_name = "api"

urlpatterns = [
    path("fiestas", views.fiestas_collection, name="fiestas-collection"),
    path(
        "invitados/<int:invitado_id>/aceptar",
        views.invitado_aceptar,
        name="invitado-aceptar",
    ),
    path(
        "invitados/<int:invitado_id>/rechazar",
        views.invitado_rechazar,
        name="invitado-rechazar",
    ),
]
