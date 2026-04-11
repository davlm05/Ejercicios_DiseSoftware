"""REST API views for Fiestas Clandestinas.

These views are intentionally thin: they parse the incoming JSON, delegate to
the services layer (``fiestas_core.services``), and translate domain
exceptions into HTTP responses. They never touch repositories or models.
"""
from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from django.http import HttpRequest, HttpResponseNotAllowed, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from apps.api.serializers import fiesta_to_dict, invitado_to_dict
from fiestas_core.exceptions import (
    CapacidadExcedidaError,
    EstadoInvalidoError,
    NotFoundError,
    ValidationError,
)
from fiestas_core.services import FiestaService, InvitadoService

_fiesta_service = FiestaService()
_invitado_service = InvitadoService()


# ---------- helpers ---------------------------------------------------------

def _error(message: str, status: int = 400) -> JsonResponse:
    return JsonResponse({"error": message}, status=status)


def _parse_json_body(request: HttpRequest) -> dict[str, Any]:
    if not request.body:
        return {}
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"invalid JSON body: {exc.msg}") from exc
    if not isinstance(data, dict):
        raise ValidationError("JSON body must be an object")
    return data


def _parse_fecha(raw: Any) -> datetime:
    if not isinstance(raw, str) or not raw:
        raise ValidationError("fecha es requerida (ISO 8601 string)")
    try:
        # accept both "...Z" and "...+00:00" forms
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValidationError(f"fecha inválida: {exc}") from exc


# ---------- endpoints -------------------------------------------------------

@csrf_exempt
def fiestas_collection(request: HttpRequest) -> JsonResponse:
    """GET /api/fiestas — list available fiestas.

    POST /api/fiestas — create a new fiesta with location and capacity.
    """
    if request.method == "GET":
        fiestas = _fiesta_service.listar_disponibles()
        return JsonResponse(
            {"fiestas": [fiesta_to_dict(f) for f in fiestas]},
            status=200,
        )

    if request.method == "POST":
        try:
            payload = _parse_json_body(request)
            fecha = _parse_fecha(payload.get("fecha"))
            fiesta = _fiesta_service.crear(
                nombre=payload.get("nombre", ""),
                descripcion=payload.get("descripcion", ""),
                ubicacion_texto=payload.get("ubicacion_texto", ""),
                latitud=_as_float(payload.get("latitud"), "latitud"),
                longitud=_as_float(payload.get("longitud"), "longitud"),
                capacidad_max=_as_int(payload.get("capacidad_max"), "capacidad_max"),
                fecha=fecha,
                host=payload.get("host", ""),
            )
        except ValidationError as exc:
            return _error(str(exc), 400)
        return JsonResponse(fiesta_to_dict(fiesta), status=201)

    return HttpResponseNotAllowed(["GET", "POST"])


@csrf_exempt
@require_http_methods(["POST"])
def invitado_aceptar(request: HttpRequest, invitado_id: int) -> JsonResponse:
    """POST /api/invitados/<id>/aceptar — accept an invitation."""
    try:
        invitado = _invitado_service.aceptar(invitado_id)
    except NotFoundError as exc:
        return _error(str(exc), 404)
    except (EstadoInvalidoError, CapacidadExcedidaError) as exc:
        return _error(str(exc), 409)
    return JsonResponse(invitado_to_dict(invitado), status=200)


@csrf_exempt
@require_http_methods(["POST"])
def invitado_rechazar(request: HttpRequest, invitado_id: int) -> JsonResponse:
    """POST /api/invitados/<id>/rechazar — decline an invitation."""
    try:
        invitado = _invitado_service.rechazar(invitado_id)
    except NotFoundError as exc:
        return _error(str(exc), 404)
    except EstadoInvalidoError as exc:
        return _error(str(exc), 409)
    return JsonResponse(invitado_to_dict(invitado), status=200)


# ---------- local coercion helpers -----------------------------------------

def _as_float(value: Any, field: str) -> float:
    if value is None:
        raise ValidationError(f"{field} es requerido")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{field} debe ser numérico") from exc


def _as_int(value: Any, field: str) -> int:
    if value is None:
        raise ValidationError(f"{field} es requerido")
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{field} debe ser entero") from exc
    return parsed
