"""Repository for Invitado — wraps ``Invitado.objects`` queries."""
from __future__ import annotations

from typing import Iterable, Optional

from fiestas_core.models import Invitado


class InvitadoRepository:
    @staticmethod
    def create(*, fiesta_id: int, nombre: str, contacto: str = "") -> Invitado:
        return Invitado.objects.create(
            fiesta_id=fiesta_id,
            nombre=nombre,
            contacto=contacto,
        )

    @staticmethod
    def get_by_id(invitado_id: int) -> Optional[Invitado]:
        return (
            Invitado.objects.select_related("fiesta")
            .filter(pk=invitado_id)
            .first()
        )

    @staticmethod
    def list_by_fiesta(fiesta_id: int) -> Iterable[Invitado]:
        return list(Invitado.objects.filter(fiesta_id=fiesta_id))

    @staticmethod
    def list_pending() -> Iterable[Invitado]:
        return list(
            Invitado.objects.select_related("fiesta")
            .filter(estado=Invitado.ESTADO_PENDING)
            .order_by("fiesta__fecha")
        )

    @staticmethod
    def set_estado(invitado_id: int, nuevo_estado: str) -> Invitado:
        invitado = Invitado.objects.select_related("fiesta").get(pk=invitado_id)
        invitado.estado = nuevo_estado
        invitado.save(update_fields=["estado"])
        return invitado
