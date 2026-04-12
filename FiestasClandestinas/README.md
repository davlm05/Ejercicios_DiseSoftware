# Fiestas Clandestinas

> Ejercicio 5 · Diseño de Software · TEC 2026
> Responsable: Jose Isaac Corrales Cascante

Monolito Django con server-side rendering para publicar fiestas clandestinas
en casas o fincas, aceptar invitados y consultar ubicaciones.

## Topología

```
┌─────────────────────────────────────────────────────────┐
│             Monolito Django (un proyecto)              │
│                                                         │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   api    │    │  invitados   │    │ localizacion │  │
│  │  (REST)  │    │   (SSR UI)   │    │   (SSR UI)   │  │
│  │ :8000    │    │   :8001      │    │    :8002     │  │
│  └─────┬────┘    └──────┬───────┘    └──────┬───────┘  │
│        │                │                   │          │
│        └───────┬────────┴───────────┬───────┘          │
│                ▼                    ▼                   │
│         ┌──────────────────────────────────┐           │
│         │          services                │           │
│         │      (business logic)            │           │
│         └──────────────┬───────────────────┘           │
│                        ▼                               │
│         ┌──────────────────────────────────┐           │
│         │         repositories             │           │
│         └──────────────┬───────────────────┘           │
│                        ▼                               │
│         ┌──────────────────────────────────┐           │
│         │     models (Django ORM)          │           │
│         └──────────────┬───────────────────┘           │
│                        ▼                               │
│                  ┌────────────┐                        │
│                  │   SQLite   │                        │
│                  └────────────┘                        │
└─────────────────────────────────────────────────────────┘
```

**Punto clave:** es un solo proyecto Django. Las tres superficies (api,
invitados, localización) pueden correr como procesos independientes cambiando
la variable `DJANGO_BUNDLE`. Comparten modelos, servicios, repositorios y la
misma base de datos SQLite.

## Estructura del proyecto

```
FiestasClandestinas/
├── manage.py
├── requirements.txt
├── fiestas_project/             # Django project config
│   ├── settings.py              #   BUNDLE switch + INSTALLED_APPS
│   ├── urls.py                  #   monolito completo
│   ├── urls_api.py              #   solo REST
│   ├── urls_invitados.py        #   solo frontend invitados
│   └── urls_localizacion.py     #   solo frontend localización
├── fiestas_core/                # core domain
│   ├── models.py                #   Fiesta, Invitado
│   ├── repositories/            #   acceso a datos (único punto al ORM)
│   │   ├── fiesta_repository.py
│   │   └── invitado_repository.py
│   ├── services/                #   lógica de negocio
│   │   ├── fiesta_service.py
│   │   └── invitado_service.py
│   ├── exceptions.py            #   excepciones de dominio
│   └── fixtures/seed.json       #   datos iniciales (4 fiestas, 5 invitados)
├── apps/
│   ├── api/                     #   REST endpoints
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   ├── invitados/               #   frontend SSR — aceptar invitaciones
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── templates/invitados/
│   └── localizacion/            #   frontend SSR — consultar ubicaciones
│       ├── views.py
│       ├── urls.py
│       └── templates/localizacion/
├── scripts/                     #   runners .sh y .bat por bundle
├── tests/                       #   smoke tests por capa
├── PLAN.md                      #   plan de implementación
├── AGENTS.md                    #   agentes de IA usados
└── GIT_FLOW.md                  #   política de branches
```

## Requisitos

- Python 3.11+
- pip (incluido con Python)

No hay dependencias de JavaScript ni bundlers de frontend.

## Setup rápido

```bash
cd FiestasClandestinas

# 1. Crear y activar virtualenv
python -m venv .venv

# Linux / macOS / Git Bash:
source .venv/bin/activate
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Migraciones + seed
python manage.py migrate
python manage.py loaddata seed.json
```

## Correr cada bundle

Cada bundle es un proceso `runserver` con `DJANGO_BUNDLE` distinto:

| Bundle | Puerto | Variable | Qué expone |
|---|---|---|---|
| **all** (monolito) | 8000 | `DJANGO_BUNDLE=all` | Todo junto: API + invitados + localización + admin |
| **api** | 8000 | `DJANGO_BUNDLE=api` | Solo `POST /api/fiestas` y `GET /api/fiestas` |
| **invitados** | 8001 | `DJANGO_BUNDLE=invitados` | Solo el frontend SSR de invitaciones |
| **localizacion** | 8002 | `DJANGO_BUNDLE=localizacion` | Solo el frontend SSR de localización |

### Con scripts

```bash
# Monolito completo:
bash scripts/run_all.sh         # o scripts\run_all.bat en CMD

# Solo la API:
bash scripts/run_api.sh         # o scripts\run_api.bat

# Solo invitados (puerto 8001):
bash scripts/run_invitados.sh   # o scripts\run_invitados.bat

# Solo localización (puerto 8002):
bash scripts/run_localizacion.sh  # o scripts\run_localizacion.bat
```

### Manual (sin scripts)

```bash
# Monolito:
python manage.py runserver 8000

# Solo API:
DJANGO_BUNDLE=api python manage.py runserver 8000

# Solo invitados:
DJANGO_BUNDLE=invitados python manage.py runserver 8001

# Solo localización:
DJANGO_BUNDLE=localizacion python manage.py runserver 8002
```

En **Windows CMD** reemplazar `VARIABLE=valor comando` por:
```cmd
set DJANGO_BUNDLE=api
python manage.py runserver 8000
```

## Modelo de datos

```
Fiesta
  id               PK
  nombre           string
  descripcion      text
  ubicacion_texto  string     "Finca La Neblina, Cartago"
  latitud          float
  longitud         float
  capacidad_max    int
  fecha            datetime
  host             string
  created_at       datetime

Invitado
  id         PK
  fiesta     FK → Fiesta
  nombre     string
  contacto   string
  estado     enum(pending, accepted, declined)
  created_at datetime
```

## API REST

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/fiestas` | Lista fiestas con `fecha >= now` |
| `POST` | `/api/fiestas` | Crea una fiesta (body JSON) |
| `POST` | `/api/invitados/<id>/aceptar` | Acepta una invitación pendiente |
| `POST` | `/api/invitados/<id>/rechazar` | Rechaza una invitación pendiente |

### Ejemplo: crear una fiesta

```bash
curl -X POST http://localhost:8000/api/fiestas \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Rave en la montaña",
    "ubicacion_texto": "Finca La Neblina, Cartago",
    "latitud": 9.8644,
    "longitud": -83.9194,
    "capacidad_max": 80,
    "fecha": "2026-06-14T22:00:00Z",
    "host": "DJ Volcán"
  }'
```

## Reglas de negocio

- Una fiesta no puede tener más invitados aceptados que su `capacidad_max`.
- Un invitado solo puede pasar de `pending` a `accepted` o `declined` (no se puede revertir).
- `GET /api/fiestas` y el frontend de localización solo muestran fiestas futuras.
- Coordenadas validadas: latitud `[-90, 90]`, longitud `[-180, 180]`.

## Tests

```bash
python manage.py test tests -v 1
```

34 tests cubren: services (validaciones, capacidad, estados), API (POST/GET, errores 400/404/409), y ambos frontends SSR (render de templates, accept/reject via form POST, redirects).

## Capas y separación de responsabilidades

| Capa | Puede importar | No puede importar |
|---|---|---|
| views (api, invitados, localizacion) | services, exceptions | repositories, models |
| services | repositories, exceptions | models directamente (via repos) |
| repositories | models | nada de capas superiores |
| models | solo Django ORM | nada |

Esta separación permite que si se cambia el storage (de SQLite a Postgres, o a un servicio externo), solo se reescribe `repositories/`.

## Documentos adicionales

| Documento | Contenido |
|---|---|
| [`PLAN.md`](PLAN.md) | Plan detallado de implementación con fases y decisiones de diseño |
| [`AGENTS.md`](AGENTS.md) | Agentes de IA especializados usados para generar el código |
| [`GIT_FLOW.md`](GIT_FLOW.md) | Política de branches, convenciones de commit, y orden de merges |
