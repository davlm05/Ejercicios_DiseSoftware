"""Smoke tests for the REST API endpoints."""
import json
from datetime import timedelta

from django.test import Client, TestCase
from django.utils import timezone

from fiestas_core.services import FiestaService, InvitadoService


def _future_iso(days: int = 7) -> str:
    return (timezone.now() + timedelta(days=days)).isoformat()


class PostFiestasTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = "/api/fiestas"

    def _valid_payload(self, **overrides) -> dict:
        base = dict(
            nombre="Party Test",
            descripcion="desc",
            ubicacion_texto="Somewhere",
            latitud=9.9,
            longitud=-84.0,
            capacidad_max=40,
            fecha=_future_iso(),
            host="Host Test",
        )
        base.update(overrides)
        return base

    def test_post_ok_returns_201(self):
        resp = self.client.post(
            self.url,
            data=json.dumps(self._valid_payload()),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 201)
        body = resp.json()
        self.assertIn("id", body)
        self.assertEqual(body["nombre"], "Party Test")
        self.assertEqual(body["capacidad_max"], 40)

    def test_post_invalid_json_returns_400(self):
        resp = self.client.post(
            self.url, data="not json", content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)

    def test_post_missing_field_returns_400(self):
        payload = self._valid_payload()
        del payload["nombre"]
        resp = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)

    def test_post_bad_latitud_returns_400(self):
        resp = self.client.post(
            self.url,
            data=json.dumps(self._valid_payload(latitud=200)),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 400)


class GetFiestasTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = "/api/fiestas"
        self.service = FiestaService()

    def test_empty_list(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"fiestas": []})

    def test_lists_only_available(self):
        self.service.crear(
            nombre="Futura",
            ubicacion_texto="X",
            latitud=0,
            longitud=0,
            capacidad_max=10,
            fecha=timezone.now() + timedelta(days=5),
            host="H",
        )
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        fiestas = resp.json()["fiestas"]
        self.assertEqual(len(fiestas), 1)
        self.assertEqual(fiestas[0]["nombre"], "Futura")


class InvitadoAceptarRechazarTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.fiesta_service = FiestaService()
        self.invitado_service = InvitadoService()
        self.fiesta = self.fiesta_service.crear(
            nombre="F",
            ubicacion_texto="X",
            latitud=0,
            longitud=0,
            capacidad_max=2,
            fecha=timezone.now() + timedelta(days=3),
            host="H",
        )

    def test_aceptar_ok(self):
        inv = self.invitado_service.registrar(
            fiesta_id=self.fiesta.pk, nombre="Ana"
        )
        resp = self.client.post(f"/api/invitados/{inv.pk}/aceptar")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["estado"], "accepted")

    def test_aceptar_not_found(self):
        resp = self.client.post("/api/invitados/9999/aceptar")
        self.assertEqual(resp.status_code, 404)

    def test_aceptar_llena_devuelve_409(self):
        for nombre in ("A", "B"):
            inv = self.invitado_service.registrar(
                fiesta_id=self.fiesta.pk, nombre=nombre
            )
            self.invitado_service.aceptar(inv.pk)
        tercero = self.invitado_service.registrar(
            fiesta_id=self.fiesta.pk, nombre="C"
        )
        resp = self.client.post(f"/api/invitados/{tercero.pk}/aceptar")
        self.assertEqual(resp.status_code, 409)

    def test_rechazar_ok(self):
        inv = self.invitado_service.registrar(
            fiesta_id=self.fiesta.pk, nombre="Ana"
        )
        resp = self.client.post(f"/api/invitados/{inv.pk}/rechazar")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["estado"], "declined")
