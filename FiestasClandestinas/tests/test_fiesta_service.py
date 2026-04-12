"""Smoke tests for FiestaService business rules."""
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from fiestas_core.exceptions import NotFoundError, ValidationError
from fiestas_core.services import FiestaService


def _valid_payload(**overrides):
    base = dict(
        nombre="Test Fiesta",
        ubicacion_texto="Ubicación X",
        latitud=9.9,
        longitud=-84.0,
        capacidad_max=10,
        fecha=timezone.now() + timedelta(days=7),
        host="Host Test",
    )
    base.update(overrides)
    return base


class FiestaServiceTests(TestCase):
    def setUp(self):
        self.service = FiestaService()

    def test_crear_ok(self):
        fiesta = self.service.crear(**_valid_payload())
        self.assertIsNotNone(fiesta.pk)
        self.assertEqual(fiesta.nombre, "Test Fiesta")

    def test_crear_rechaza_capacidad_cero(self):
        with self.assertRaises(ValidationError):
            self.service.crear(**_valid_payload(capacidad_max=0))

    def test_crear_rechaza_latitud_invalida(self):
        with self.assertRaises(ValidationError):
            self.service.crear(**_valid_payload(latitud=120))

    def test_crear_rechaza_nombre_vacio(self):
        with self.assertRaises(ValidationError):
            self.service.crear(**_valid_payload(nombre="   "))

    def test_listar_disponibles_excluye_pasadas(self):
        self.service.crear(
            **_valid_payload(fecha=timezone.now() + timedelta(days=3))
        )
        self.service.crear(
            **_valid_payload(
                nombre="Futura",
                fecha=timezone.now() + timedelta(days=30),
            )
        )
        disponibles = list(self.service.listar_disponibles())
        self.assertEqual(len(disponibles), 2)

    def test_obtener_no_existente(self):
        with self.assertRaises(NotFoundError):
            self.service.obtener(999)

    def test_cupos_disponibles(self):
        fiesta = self.service.crear(**_valid_payload(capacidad_max=5))
        self.assertEqual(self.service.cupos_disponibles(fiesta.pk), 5)
