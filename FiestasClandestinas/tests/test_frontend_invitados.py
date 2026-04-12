"""Smoke tests for the invitados SSR frontend."""
from datetime import timedelta

from django.test import Client, TestCase
from django.utils import timezone

from fiestas_core.models import Invitado
from fiestas_core.services import FiestaService, InvitadoService


class FrontendInvitadosTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.fiesta_service = FiestaService()
        self.invitado_service = InvitadoService()
        self.fiesta = self.fiesta_service.crear(
            nombre="Rave Test",
            ubicacion_texto="Ubicación Test",
            latitud=9.9,
            longitud=-84.0,
            capacidad_max=10,
            fecha=timezone.now() + timedelta(days=3),
            host="DJ Test",
        )
        self.invitado = self.invitado_service.registrar(
            fiesta_id=self.fiesta.pk, nombre="Ana Test"
        )

    def test_listar_muestra_pendientes(self):
        resp = self.client.get("/invitados/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Rave Test")
        self.assertContains(resp, "Ana Test")
        self.assertContains(resp, "Aceptar")
        self.assertContains(resp, "Rechazar")

    def test_aceptar_cambia_estado_y_redirige(self):
        resp = self.client.post(f"/invitados/{self.invitado.pk}/aceptar")
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "/invitados/")
        self.invitado.refresh_from_db()
        self.assertEqual(self.invitado.estado, Invitado.ESTADO_ACCEPTED)

    def test_rechazar_cambia_estado(self):
        resp = self.client.post(f"/invitados/{self.invitado.pk}/rechazar")
        self.assertEqual(resp.status_code, 302)
        self.invitado.refresh_from_db()
        self.assertEqual(self.invitado.estado, Invitado.ESTADO_DECLINED)

    def test_aceptar_get_no_permitido(self):
        resp = self.client.get(f"/invitados/{self.invitado.pk}/aceptar")
        self.assertEqual(resp.status_code, 405)

    def test_listar_vacio(self):
        # rechazamos el único pendiente
        self.client.post(f"/invitados/{self.invitado.pk}/rechazar")
        resp = self.client.get("/invitados/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Sin invitaciones pendientes")
