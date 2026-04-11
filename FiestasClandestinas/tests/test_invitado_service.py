"""Smoke tests for InvitadoService business rules."""
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from fiestas_core.exceptions import (
    CapacidadExcedidaError,
    EstadoInvalidoError,
    NotFoundError,
    ValidationError,
)
from fiestas_core.models import Invitado
from fiestas_core.services import FiestaService, InvitadoService


class InvitadoServiceTests(TestCase):
    def setUp(self):
        self.fiesta_service = FiestaService()
        self.invitado_service = InvitadoService()
        self.fiesta = self.fiesta_service.crear(
            nombre="Fiesta Test",
            ubicacion_texto="Ubicación Test",
            latitud=9.9,
            longitud=-84.0,
            capacidad_max=2,
            fecha=timezone.now() + timedelta(days=5),
            host="Host",
        )

    def test_registrar_ok(self):
        invitado = self.invitado_service.registrar(
            fiesta_id=self.fiesta.pk, nombre="Ana"
        )
        self.assertEqual(invitado.estado, Invitado.ESTADO_PENDING)
        self.assertEqual(invitado.fiesta_id, self.fiesta.pk)

    def test_registrar_fiesta_inexistente(self):
        with self.assertRaises(NotFoundError):
            self.invitado_service.registrar(fiesta_id=999, nombre="X")

    def test_registrar_nombre_vacio(self):
        with self.assertRaises(ValidationError):
            self.invitado_service.registrar(fiesta_id=self.fiesta.pk, nombre=" ")

    def test_aceptar_cambia_estado(self):
        inv = self.invitado_service.registrar(
            fiesta_id=self.fiesta.pk, nombre="Ana"
        )
        aceptado = self.invitado_service.aceptar(inv.pk)
        self.assertEqual(aceptado.estado, Invitado.ESTADO_ACCEPTED)

    def test_aceptar_rechaza_capacidad_excedida(self):
        for nombre in ("A", "B"):
            inv = self.invitado_service.registrar(
                fiesta_id=self.fiesta.pk, nombre=nombre
            )
            self.invitado_service.aceptar(inv.pk)
        tercero = self.invitado_service.registrar(
            fiesta_id=self.fiesta.pk, nombre="C"
        )
        with self.assertRaises(CapacidadExcedidaError):
            self.invitado_service.aceptar(tercero.pk)

    def test_aceptar_dos_veces_falla(self):
        inv = self.invitado_service.registrar(
            fiesta_id=self.fiesta.pk, nombre="Ana"
        )
        self.invitado_service.aceptar(inv.pk)
        with self.assertRaises(EstadoInvalidoError):
            self.invitado_service.aceptar(inv.pk)

    def test_rechazar_ok(self):
        inv = self.invitado_service.registrar(
            fiesta_id=self.fiesta.pk, nombre="Ana"
        )
        rechazado = self.invitado_service.rechazar(inv.pk)
        self.assertEqual(rechazado.estado, Invitado.ESTADO_DECLINED)
