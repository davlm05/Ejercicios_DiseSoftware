"""SSR views for the localización frontend.

Lets a user browse available fiestas and see their coordinates, host, and
remaining capacity. Like the invitados frontend, these views only call the
service layer.
"""
from __future__ import annotations

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from fiestas_core.exceptions import NotFoundError
from fiestas_core.services import FiestaService

_fiesta_service = FiestaService()


def listar(request: HttpRequest) -> HttpResponse:
    """GET /localizacion/ — list every available fiesta."""
    fiestas = _fiesta_service.listar_disponibles()
    enriched = [
        {
            "fiesta": f,
            "cupos_disponibles": _fiesta_service.cupos_disponibles(f.pk),
        }
        for f in fiestas
    ]
    return render(
        request,
        "localizacion/list.html",
        {"fiestas": enriched},
    )


def detalle(request: HttpRequest, fiesta_id: int) -> HttpResponse:
    """GET /localizacion/<id> — detail view for one fiesta."""
    try:
        fiesta = _fiesta_service.obtener(fiesta_id)
    except NotFoundError as exc:
        raise Http404(str(exc)) from exc
    cupos = _fiesta_service.cupos_disponibles(fiesta_id)
    return render(
        request,
        "localizacion/detail.html",
        {"fiesta": fiesta, "cupos_disponibles": cupos},
    )
