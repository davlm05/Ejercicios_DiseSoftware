"""Business logic for Invitado entities.

Rules enforced here:
- Cannot register an invitado to a non-existent fiesta.
- Cannot accept/reject an invitado that is not in ``pending`` state.
- Cannot accept an invitado if the fiesta is already at capacity.
"""
from __future__ import annotations

from typing import Iterable, Optional

from fiestas_core.exceptions import (
    CapacidadExcedidaError,
    EstadoInvalidoError,
    NotFoundError,
    ValidationError,
)
from fiestas_core.models import Invitado
from fiestas_core.repositories import FiestaRepository, InvitadoRepository


class InvitadoService:
    def __init__(
        self,
        invitado_repo: Optional[InvitadoRepository] = None,
        fiesta_repo: Optional[FiestaRepository] = None,
    ) -> None:
        self.invitado_repo = invitado_repo or InvitadoRepository()
        self.fiesta_repo = fiesta_repo or FiestaRepository()

    # ---------- commands ----------
    def registrar(self, *, fiesta_id: int, nombre: str, contacto: str = "") -> Invitado:
        if not nombre or not nombre.strip():
            raise ValidationError("nombre no puede estar vacío")
        fiesta = self.fiesta_repo.get_by_id(fiesta_id)
        if fiesta is None:
            raise NotFoundError(f"Fiesta {fiesta_id} no existe")
        return self.invitado_repo.create(
            fiesta_id=fiesta_id,
            nombre=nombre.strip(),
            contacto=contacto.strip(),
        )

    def aceptar(self, invitado_id: int) -> Invitado:
        invitado = self._get_pending(invitado_id)
        aceptados = self.fiesta_repo.count_accepted_invitados(invitado.fiesta_id)
        if aceptados >= invitado.fiesta.capacidad_max:
            raise CapacidadExcedidaError(
                f"Fiesta '{invitado.fiesta.nombre}' está llena "
                f"({aceptados}/{invitado.fiesta.capacidad_max})"
            )
        return self.invitado_repo.set_estado(invitado_id, Invitado.ESTADO_ACCEPTED)

    def rechazar(self, invitado_id: int) -> Invitado:
        self._get_pending(invitado_id)
        return self.invitado_repo.set_estado(invitado_id, Invitado.ESTADO_DECLINED)

    # ---------- queries ----------
    def listar_pendientes(self) -> Iterable[Invitado]:
        return self.invitado_repo.list_pending()

    def listar_por_fiesta(self, fiesta_id: int) -> Iterable[Invitado]:
        return self.invitado_repo.list_by_fiesta(fiesta_id)

    # ---------- helpers ----------
    def _get_pending(self, invitado_id: int) -> Invitado:
        invitado = self.invitado_repo.get_by_id(invitado_id)
        if invitado is None:
            raise NotFoundError(f"Invitado {invitado_id} no existe")
        if invitado.estado != Invitado.ESTADO_PENDING:
            raise EstadoInvalidoError(
                f"Invitado {invitado_id} está en estado '{invitado.estado}' "
                f"y no puede cambiar"
            )
        return invitado
