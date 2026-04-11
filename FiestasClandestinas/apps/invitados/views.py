"""SSR views for the invitados frontend.

This frontend lets a guest see their pending invitations and accept or reject
them. All the rendering is server-side with Django templates — there is no
JavaScript bundler involved.

Rule of the monolith: these views only call the service layer
(``fiestas_core.services``). They never touch repositories or models directly.
"""
from __future__ import annotations

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from fiestas_core.exceptions import (
    CapacidadExcedidaError,
    EstadoInvalidoError,
    NotFoundError,
)
from fiestas_core.services import InvitadoService

_invitado_service = InvitadoService()


def listar(request: HttpRequest) -> HttpResponse:
    """GET /invitados/ — list every pending invitation."""
    pendientes = _invitado_service.listar_pendientes()
    return render(
        request,
        "invitados/list.html",
        {"invitados": pendientes},
    )


@require_http_methods(["POST"])
def aceptar(request: HttpRequest, invitado_id: int) -> HttpResponse:
    try:
        invitado = _invitado_service.aceptar(invitado_id)
    except NotFoundError as exc:
        messages.error(request, str(exc))
    except EstadoInvalidoError as exc:
        messages.error(request, str(exc))
    except CapacidadExcedidaError as exc:
        messages.error(request, str(exc))
    else:
        messages.success(
            request,
            f"{invitado.nombre} aceptó la invitación a {invitado.fiesta.nombre}.",
        )
    return redirect("invitados:listar")


@require_http_methods(["POST"])
def rechazar(request: HttpRequest, invitado_id: int) -> HttpResponse:
    try:
        invitado = _invitado_service.rechazar(invitado_id)
    except NotFoundError as exc:
        messages.error(request, str(exc))
    except EstadoInvalidoError as exc:
        messages.error(request, str(exc))
    else:
        messages.success(
            request,
            f"{invitado.nombre} rechazó la invitación a {invitado.fiesta.nombre}.",
        )
    return redirect("invitados:listar")
