"""Django models for Fiestas Clandestinas.

This module is the *model* layer. Only repositories (``fiestas_core.repositories``)
are allowed to import from here. Upper layers (services, api views, SSR views)
must go through repositories, never touch ``Fiesta.objects`` / ``Invitado.objects``
directly.
"""
from django.db import models


class Fiesta(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    ubicacion_texto = models.CharField(max_length=300)
    latitud = models.FloatField()
    longitud = models.FloatField()
    capacidad_max = models.PositiveIntegerField()
    fecha = models.DateTimeField()
    host = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["fecha"]

    def __str__(self) -> str:
        return f"{self.nombre} — {self.fecha:%Y-%m-%d %H:%M}"


class Invitado(models.Model):
    ESTADO_PENDING = "pending"
    ESTADO_ACCEPTED = "accepted"
    ESTADO_DECLINED = "declined"
    ESTADO_CHOICES = [
        (ESTADO_PENDING, "Pendiente"),
        (ESTADO_ACCEPTED, "Aceptado"),
        (ESTADO_DECLINED, "Rechazado"),
    ]

    fiesta = models.ForeignKey(
        Fiesta, on_delete=models.CASCADE, related_name="invitados"
    )
    nombre = models.CharField(max_length=200)
    contacto = models.CharField(max_length=200, blank=True)
    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default=ESTADO_PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["fiesta", "estado"]),
        ]

    def __str__(self) -> str:
        return f"{self.nombre} → {self.fiesta.nombre} ({self.estado})"
