"""Repository for Fiesta — wraps ``Fiesta.objects`` queries.

All ORM calls for the Fiesta entity live here. If the storage changes
(Postgres, another ORM, a remote service), only this file needs to be
rewritten.
"""
from __future__ import annotations

from typing import Iterable, Optional

from django.utils import timezone

from fiestas_core.models import Fiesta, Invitado


class FiestaRepository:
    @staticmethod
    def create(
        *,
        nombre: str,
        ubicacion_texto: str,
        latitud: float,
        longitud: float,
        capacidad_max: int,
        fecha,
        host: str,
        descripcion: str = "",
    ) -> Fiesta:
        return Fiesta.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            ubicacion_texto=ubicacion_texto,
            latitud=latitud,
            longitud=longitud,
            capacidad_max=capacidad_max,
            fecha=fecha,
            host=host,
        )

    @staticmethod
    def get_by_id(fiesta_id: int) -> Optional[Fiesta]:
        return Fiesta.objects.filter(pk=fiesta_id).first()

    @staticmethod
    def list_all() -> Iterable[Fiesta]:
        return list(Fiesta.objects.all())

    @staticmethod
    def list_available() -> Iterable[Fiesta]:
        """Fiestas whose date is in the future (available for new invitados)."""
        return list(Fiesta.objects.filter(fecha__gte=timezone.now()).order_by("fecha"))

    @staticmethod
    def count_accepted_invitados(fiesta_id: int) -> int:
        """Number of invitados with estado='accepted' for a given fiesta."""
        return Invitado.objects.filter(
            fiesta_id=fiesta_id,
            estado=Invitado.ESTADO_ACCEPTED,
        ).count()
