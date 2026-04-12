"""URL patterns for the localización SSR frontend."""
from django.urls import path

from apps.localizacion import views

app_name = "localizacion"

urlpatterns = [
    path("", views.listar, name="listar"),
    path("<int:fiesta_id>", views.detalle, name="detalle"),
]
