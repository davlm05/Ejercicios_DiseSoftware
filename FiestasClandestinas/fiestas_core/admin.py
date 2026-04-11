from django.contrib import admin

from fiestas_core.models import Fiesta, Invitado


@admin.register(Fiesta)
class FiestaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "fecha", "host", "capacidad_max")
    search_fields = ("nombre", "host", "ubicacion_texto")
    ordering = ("fecha",)


@admin.register(Invitado)
class InvitadoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "fiesta", "estado", "created_at")
    list_filter = ("estado",)
    search_fields = ("nombre", "contacto")
