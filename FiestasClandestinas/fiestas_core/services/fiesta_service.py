"""Business logic for Fiesta entities.

Rules enforced here:
- ``capacidad_max`` must be strictly positive.
- latitud must be in [-90, 90].
- longitud must be in [-180, 180].
- ``nombre``, ``ubicacion_texto`` and ``host`` cannot be blank.
"""
from __future__ import annotations

from datetime import datetime
from typing import Iterable, Optional

from fiestas_core.exceptions import NotFoundError, ValidationError
from fiestas_core.models import Fiesta
from fiestas_core.repositories import FiestaRepository


class FiestaService:
    def __init__(self, repo: Optional[FiestaRepository] = None) -> None:
        self.repo = repo or FiestaRepository()

    # ---------- commands ----------
    def crear(
        self,
        *,
        nombre: str,
        ubicacion_texto: str,
        latitud: float,
        longitud: float,
        capacidad_max: int,
        fecha: datetime,
        host: str,
        descripcion: str = "",
    ) -> Fiesta:
        self._validate(
            nombre=nombre,
            ubicacion_texto=ubicacion_texto,
            latitud=latitud,
            longitud=longitud,
            capacidad_max=capacidad_max,
            host=host,
        )
        return self.repo.create(
            nombre=nombre.strip(),
            ubicacion_texto=ubicacion_texto.strip(),
            latitud=latitud,
            longitud=longitud,
            capacidad_max=capacidad_max,
            fecha=fecha,
            host=host.strip(),
            descripcion=descripcion.strip(),
        )

    # ---------- queries ----------
    def listar_disponibles(self) -> Iterable[Fiesta]:
        return self.repo.list_available()

    def listar_todas(self) -> Iterable[Fiesta]:
        return self.repo.list_all()

    def obtener(self, fiesta_id: int) -> Fiesta:
        fiesta = self.repo.get_by_id(fiesta_id)
        if fiesta is None:
            raise NotFoundError(f"Fiesta {fiesta_id} no existe")
        return fiesta

    def cupos_disponibles(self, fiesta_id: int) -> int:
        fiesta = self.obtener(fiesta_id)
        aceptados = self.repo.count_accepted_invitados(fiesta_id)
        return max(fiesta.capacidad_max - aceptados, 0)

    # ---------- helpers ----------
    @staticmethod
    def _validate(
        *,
        nombre: str,
        ubicacion_texto: str,
        latitud: float,
        longitud: float,
        capacidad_max: int,
        host: str,
    ) -> None:
        if not nombre or not nombre.strip():
            raise ValidationError("nombre no puede estar vacío")
        if not ubicacion_texto or not ubicacion_texto.strip():
            raise ValidationError("ubicacion_texto no puede estar vacía")
        if not host or not host.strip():
            raise ValidationError("host no puede estar vacío")
        if capacidad_max is None or capacidad_max <= 0:
            raise ValidationError("capacidad_max debe ser un entero positivo")
        if not (-90 <= latitud <= 90):
            raise ValidationError("latitud fuera de rango [-90, 90]")
        if not (-180 <= longitud <= 180):
            raise ValidationError("longitud fuera de rango [-180, 180]")
