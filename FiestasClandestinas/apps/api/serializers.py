"""Plain-Python serializers for the API layer.

No DRF. These helpers convert domain models into the JSON shape exposed by
the endpoints. Keeping serialization out of the views and out of the services
makes it easier to evolve the wire format without touching business logic.
"""
from __future__ import annotations

from fiestas_core.models import Fiesta, Invitado


def fiesta_to_dict(fiesta: Fiesta) -> dict:
    return {
        "id": fiesta.id,
        "nombre": fiesta.nombre,
        "descripcion": fiesta.descripcion,
        "ubicacion_texto": fiesta.ubicacion_texto,
        "latitud": fiesta.latitud,
        "longitud": fiesta.longitud,
        "capacidad_max": fiesta.capacidad_max,
        "fecha": fiesta.fecha.isoformat(),
        "host": fiesta.host,
    }


def invitado_to_dict(invitado: Invitado) -> dict:
    return {
        "id": invitado.id,
        "nombre": invitado.nombre,
        "contacto": invitado.contacto,
        "estado": invitado.estado,
        "fiesta_id": invitado.fiesta_id,
    }
