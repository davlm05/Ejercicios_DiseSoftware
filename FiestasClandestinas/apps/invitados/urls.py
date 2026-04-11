"""URL patterns for the invitados SSR frontend.

Mounted under ``/invitados/`` by ``fiestas_project.urls`` (and is the root
of the ``invitados`` bundle when ``DJANGO_BUNDLE=invitados``).
"""
from django.urls import path

from apps.invitados import views

app_name = "invitados"

urlpatterns = [
    path("", views.listar, name="listar"),
    path("<int:invitado_id>/aceptar", views.aceptar, name="aceptar"),
    path("<int:invitado_id>/rechazar", views.rechazar, name="rechazar"),
]
