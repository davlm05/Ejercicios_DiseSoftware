# Plan de Implementación — Fiestas Clandestinas

> Ejercicio 5 · Diseño de Software · TEC 2026
> Responsable: Jose Isaac Corrales Cascante

## 1. Objetivo

Construir un **monolito Django con server-side rendering** para gestionar fiestas clandestinas en casas o fincas. El monolito debe exponer:

- Una **API** mínima para crear y listar fiestas.
- Dos **frontends SSR** (templates Django) que se pueden ejecutar como bundles independientes:
  1. Frontend de **invitados** — aceptar/rechazar invitaciones.
  2. Frontend de **localización** — consultar ubicaciones de fiestas disponibles.

Todo corre localmente con **SQLite** y un seed pequeño.

## 2. Topología

```
┌─────────────────────────────────────────────────────────┐
│             Monolito Django (un proyecto)              │
│                                                         │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   api    │    │  invitados   │    │ localizacion │  │
│  │  (REST)  │    │   (SSR UI)   │    │   (SSR UI)   │  │
│  └─────┬────┘    └──────┬───────┘    └──────┬───────┘  │
│        │                │                   │          │
│        └───────┬────────┴───────────┬───────┘          │
│                ▼                    ▼                   │
│         ┌──────────────┐    ┌──────────────┐           │
│         │   services   │    │   services   │           │
│         │ (business)   │    │ (business)   │           │
│         └──────┬───────┘    └──────┬───────┘           │
│                └─────────┬─────────┘                   │
│                          ▼                              │
│                  ┌──────────────┐                       │
│                  │ repositories │                       │
│                  └──────┬───────┘                       │
│                         ▼                               │
│                  ┌──────────────┐                       │
│                  │    models    │ (Django ORM)          │
│                  └──────┬───────┘                       │
│                         ▼                               │
│                   ┌────────────┐                        │
│                   │  SQLite    │                        │
│                   └────────────┘                        │
└─────────────────────────────────────────────────────────┘
```

**Punto clave:** es **un solo proyecto Django**, pero se pueden arrancar tres procesos distintos que exponen superficies distintas cambiando `DJANGO_BUNDLE` por variable de entorno. Esto cumple "capacidad de ejecutar bundles por separado" sin romper el monolito.

## 3. Capas

| Capa | Responsabilidad | Ubicación |
|---|---|---|
| `model` | Definición de entidades con Django ORM | `fiestas_core/models.py` |
| `repositories` | Único punto de acceso a `Fiesta.objects.*` / `Invitado.objects.*`. Devuelve DTOs o modelos, pero las capas superiores nunca importan el ORM directamente. | `fiestas_core/repositories/` |
| `services` (business logic) | Reglas: validar capacidad, cambiar estado de invitado, geolocalizar fiesta disponible, etc. Orquesta repositorios. | `fiestas_core/services/` |
| `apps/api` | Endpoints REST — usa services. | `apps/api/` |
| `apps/invitados` | Views SSR + templates para aceptar invitaciones. | `apps/invitados/` |
| `apps/localizacion` | Views SSR + templates para consultar ubicaciones. | `apps/localizacion/` |

**Regla:** las apps (`api`, `invitados`, `localizacion`) **solo hablan con services**. Nunca importan `Fiesta.objects` ni consultan el ORM directo. Esto garantiza que si mañana se migra a Postgres o a otro storage, solo cambia `repositories/`.

## 4. Modelo de datos

```python
Fiesta
  id               int PK
  nombre           str
  descripcion      str
  ubicacion_texto  str      # "Finca La Montaña, Cartago"
  latitud          float
  longitud         float
  capacidad_max    int
  fecha            datetime
  host             str
  created_at       datetime

Invitado
  id         int PK
  fiesta     FK Fiesta
  nombre     str
  contacto   str
  estado     enum('pending', 'accepted', 'declined')
  created_at datetime
```

**Reglas de negocio mínimas:**
- Una fiesta no puede tener más invitados `accepted` que `capacidad_max`.
- Un invitado solo puede aceptar si su estado actual es `pending`.
- `GET /fiestas` solo retorna fiestas cuya `fecha >= now`.

## 5. API

| Método | Ruta | Body / Query | Response | Capa que invoca |
|---|---|---|---|---|
| POST | `/api/fiestas` | JSON `{nombre, ubicacion_texto, lat, lon, capacidad_max, fecha, host}` | 201 + fiesta creada | `services.crear_fiesta` |
| GET  | `/api/fiestas` | — | 200 + lista de fiestas disponibles | `services.listar_disponibles` |
| POST | `/api/invitados/{id}/aceptar` | — | 200 / 409 si llena | `services.aceptar_invitacion` |

## 6. Rutas SSR

**Frontend invitados (`/invitados/...`)**
- `GET /invitados/` — lista de invitaciones pendientes (demo, sin auth real).
- `POST /invitados/{id}/aceptar` — form submit que llama al service.
- `POST /invitados/{id}/rechazar` — idem.

**Frontend localización (`/localizacion/...`)**
- `GET /localizacion/` — lista + mini-mapa estático con coordenadas.
- `GET /localizacion/{id}` — detalle con dirección y host.

## 7. Bundles separables

El switch vive en `fiestas_project/settings.py`:

```python
BUNDLE = os.environ.get("DJANGO_BUNDLE", "all")

if BUNDLE == "api":
    ROOT_URLCONF = "fiestas_project.urls_api"
elif BUNDLE == "invitados":
    ROOT_URLCONF = "fiestas_project.urls_invitados"
elif BUNDLE == "localizacion":
    ROOT_URLCONF = "fiestas_project.urls_localizacion"
else:
    ROOT_URLCONF = "fiestas_project.urls"   # todo junto
```

Scripts en `scripts/`:
- `run_api.sh` → `DJANGO_BUNDLE=api python manage.py runserver 8000`
- `run_invitados.sh` → `DJANGO_BUNDLE=invitados python manage.py runserver 8001`
- `run_localizacion.sh` → `DJANGO_BUNDLE=localizacion python manage.py runserver 8002`
- `run_all.sh` → `python manage.py runserver 8000` (monolito completo)
- Versiones `.ps1` y `.bat` para Windows.

Cada bundle comparte la misma DB SQLite (`db.sqlite3`) y los mismos modelos/services/repositorios — lo único que cambia es **qué URLs están expuestas**.

## 8. Fases (una feature branch por fase)

| # | Feature branch | Entregable |
|---|---|---|
| 1 | `feature/docs-and-plan` | Este `PLAN.md`, `AGENTS.md`, `GIT_FLOW.md` |
| 2 | `feature/backend-core` | `manage.py`, `settings`, apps vacías, `fiestas_core` con models + repositorios + services, migraciones, seed (`fixtures/seed.json`) |
| 3 | `feature/api-fiestas` | App `apps/api` con `POST /api/fiestas` y `GET /api/fiestas`, tests básicos |
| 4 | `feature/frontend-invitados` | App `apps/invitados` con templates y views SSR |
| 5 | `feature/frontend-localizacion` | App `apps/localizacion` con templates y views SSR |
| 6 | `feature/bundles-scripts` | `settings` con switch `DJANGO_BUNDLE`, `urls_*.py`, scripts en `scripts/` |
| 7 | `feature/readme-final` | `README.md` de presentación con diagramas y cómo correr cada bundle |

Cada feature branch mergea a `ejercicio-5-fiestas-clandestinas`. Al final, esta branch mergea a `main` (ver `GIT_FLOW.md`).

## 9. Stack y dependencias

- Python 3.11+
- Django 5.x
- `djangorestframework` (solo para la API — las vistas SSR usan templates Django puros)
- SQLite (nativo, sin driver extra)
- Sin frameworks JS ni bundlers de frontend: los "frontends" son templates server-rendered.

## 10. Qué NO vamos a hacer

- ❌ Autenticación real / OAuth — demasiado scope para un ejercicio.
- ❌ Mapas interactivos tipo Leaflet — `localizacion` muestra coordenadas y dirección en texto; si sobra tiempo, un `<iframe>` estático con OpenStreetMap.
- ❌ WebSockets / realtime.
- ❌ Dockerización — el requisito es "todo funcionando localmente" con SQLite.
- ❌ Tests exhaustivos — solo smoke tests para services y endpoints.
