"""Smoke tests for the localización SSR frontend."""
from datetime import timedelta

from django.test import Client, TestCase
from django.utils import timezone

from fiestas_core.services import FiestaService, InvitadoService


class FrontendLocalizacionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.fiesta_service = FiestaService()
        self.invitado_service = InvitadoService()
        self.fiesta = self.fiesta_service.crear(
            nombre="Bodega Underground",
            descripcion="Fiesta secreta junto al mar",
            ubicacion_texto="Puntarenas",
            latitud=9.9763,
            longitud=-84.8384,
            capacidad_max=20,
            fecha=timezone.now() + timedelta(days=7),
            host="Crew Test",
        )

    def test_listar_muestra_fiestas_disponibles(self):
        resp = self.client.get("/localizacion/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Bodega Underground")
        self.assertContains(resp, "Puntarenas")
        self.assertContains(resp, "9.9763")
        self.assertContains(resp, "-84.8384")

    def test_listar_no_muestra_fiestas_pasadas(self):
        # crear una fiesta pasada directamente via repo para saltar validación
        from fiestas_core.repositories import FiestaRepository
        FiestaRepository.create(
            nombre="Vieja",
            ubicacion_texto="X",
            latitud=0,
            longitud=0,
            capacidad_max=10,
            fecha=timezone.now() - timedelta(days=2),
            host="H",
        )
        resp = self.client.get("/localizacion/")
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, "Vieja")

    def test_detalle_ok(self):
        resp = self.client.get(f"/localizacion/{self.fiesta.pk}")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Bodega Underground")
        self.assertContains(resp, "Crew Test")
        self.assertContains(resp, "Fiesta secreta")

    def test_detalle_not_found(self):
        resp = self.client.get("/localizacion/99999")
        self.assertEqual(resp.status_code, 404)

    def test_cupos_disponibles_decrece_con_accepted(self):
        for nombre in ("A", "B"):
            inv = self.invitado_service.registrar(
                fiesta_id=self.fiesta.pk, nombre=nombre
            )
            self.invitado_service.aceptar(inv.pk)
        resp = self.client.get("/localizacion/")
        self.assertContains(resp, "18 cupos")  # 20 - 2
