# Fiestas Clandestinas

> Ejercicio 5 · Diseño de Software · TEC 2026
> Responsable: Jose Isaac Corrales Cascante

Monolito Django con server-side rendering para publicar fiestas clandestinas
en casas o fincas, aceptar invitados y consultar ubicaciones.

---

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

Es **un solo proyecto Django**. Las tres superficies (api, invitados,
localización) pueden correr como procesos independientes cambiando la variable
de entorno `DJANGO_BUNDLE`. Comparten modelos, servicios, repositorios y la
misma base de datos SQLite.

---

## Requisitos previos

Antes de empezar, verificá que tenés Python 3.11 o superior:

```bash
python --version
```

Salida esperada (ejemplo): `Python 3.14.0`

Si el comando falla o la versión es menor a 3.11, instalá Python desde
https://www.python.org/downloads/ (en Windows marcá "Add Python to PATH"
durante la instalación).

No se necesita Node.js, npm, ni ningún bundler de JavaScript.

---

## Setup paso a paso

Todos los comandos se ejecutan **desde la carpeta `FiestasClandestinas/`**.

### Paso 1 — Entrar a la carpeta

```bash
cd FiestasClandestinas
```

### Paso 2 — Crear el virtualenv

```bash
python -m venv .venv
```

Esto crea una carpeta `.venv/` con un Python aislado. Solo hay que hacerlo
una vez.

### Paso 3 — Activar el virtualenv

Elegí **una** de estas opciones según tu terminal:

**Linux / macOS / Git Bash (Windows):**
```bash
source .venv/bin/activate
```

**Windows PowerShell:**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
.venv\Scripts\activate.bat
```

Verificación: el prompt debe mostrar `(.venv)` al inicio. Ejemplo:
```
(.venv) C:\...\FiestasClandestinas>
```

### Paso 4 — Instalar Django

```bash
pip install -r requirements.txt
```

Verificación:
```bash
python -c "import django; print(django.get_version())"
```
Salida esperada: `5.2.13` (o superior 5.x).

### Paso 5 — Crear la base de datos

```bash
python manage.py migrate
```

Salida esperada (última línea): `Applying sessions.0001_initial... OK`

Esto crea el archivo `db.sqlite3` en la raíz del proyecto.

### Paso 6 — Cargar datos de ejemplo

```bash
python manage.py loaddata seed.json
```

Salida esperada: `Installed 9 object(s) from 1 fixture(s)`

Los datos cargados son 4 fiestas y 5 invitados en distintos estados.

### Paso 7 — Verificar que todo funciona

```bash
python manage.py test tests -v 1
```

Salida esperada (última línea): `OK` con 34 tests ejecutados.

---

## Correr el proyecto

### Opción A — Monolito completo (todo en un solo puerto)

```bash
python manage.py runserver 8000
```

Acceder a:
- http://localhost:8000/ — index JSON con lista de endpoints
- http://localhost:8000/invitados/ — frontend SSR de invitaciones
- http://localhost:8000/localizacion/ — frontend SSR de localización
- http://localhost:8000/api/fiestas — API REST (JSON)
- http://localhost:8000/admin/ — Django admin

### Opción B — Cada bundle por separado (en terminales distintas)

Abrir 3 terminales. En cada una activar el venv y correr:

**Terminal 1 — API (puerto 8000):**

Linux/macOS/Git Bash:
```bash
DJANGO_BUNDLE=api python manage.py runserver 8000
```

Windows PowerShell:
```powershell
$env:DJANGO_BUNDLE="api"; python manage.py runserver 8000
```

Windows CMD:
```cmd
set DJANGO_BUNDLE=api
python manage.py runserver 8000
```

**Terminal 2 — Frontend Invitados (puerto 8001):**

Linux/macOS/Git Bash:
```bash
DJANGO_BUNDLE=invitados python manage.py runserver 8001
```

Windows PowerShell:
```powershell
$env:DJANGO_BUNDLE="invitados"; python manage.py runserver 8001
```

Windows CMD:
```cmd
set DJANGO_BUNDLE=invitados
python manage.py runserver 8001
```

**Terminal 3 — Frontend Localización (puerto 8002):**

Linux/macOS/Git Bash:
```bash
DJANGO_BUNDLE=localizacion python manage.py runserver 8002
```

Windows PowerShell:
```powershell
$env:DJANGO_BUNDLE="localizacion"; python manage.py runserver 8002
```

Windows CMD:
```cmd
set DJANGO_BUNDLE=localizacion
python manage.py runserver 8002
```

### Opción C — Usando los scripts

Los scripts en `scripts/` ya configuran la variable y el puerto:

| Script (bash) | Script (Windows) | Puerto | Qué arranca |
|---|---|---|---|
| `bash scripts/run_all.sh` | `scripts\run_all.bat` | 8000 | Monolito completo |
| `bash scripts/run_api.sh` | `scripts\run_api.bat` | 8000 | Solo API REST |
| `bash scripts/run_invitados.sh` | `scripts\run_invitados.bat` | 8001 | Solo frontend invitados |
| `bash scripts/run_localizacion.sh` | `scripts\run_localizacion.bat` | 8002 | Solo frontend localización |

Cada script asume que el virtualenv ya está activado.

---

## Qué hay en cada URL

| URL | Bundle | Descripción |
|---|---|---|
| `/` | all | JSON con endpoints disponibles |
| `/invitados/` | all, invitados | Lista de invitaciones pendientes con botones Aceptar/Rechazar |
| `/invitados/<id>/aceptar` | all, invitados | POST: acepta la invitación y redirige a `/invitados/` |
| `/invitados/<id>/rechazar` | all, invitados | POST: rechaza la invitación y redirige a `/invitados/` |
| `/localizacion/` | all, localizacion | Lista de fiestas disponibles con coordenadas y link a OpenStreetMap |
| `/localizacion/<id>` | all, localizacion | Detalle de una fiesta: ubicación, host, capacidad, cupos |
| `/api/fiestas` | all, api | GET: lista fiestas futuras (JSON). POST: crea una fiesta (JSON) |
| `/api/invitados/<id>/aceptar` | all, api | POST: acepta invitación (JSON) |
| `/api/invitados/<id>/rechazar` | all, api | POST: rechaza invitación (JSON) |
| `/admin/` | all | Django admin (crear superusuario con `python manage.py createsuperuser`) |

---

## API REST — Ejemplos copy-paste

### Listar fiestas disponibles

```bash
curl http://localhost:8000/api/fiestas
```

Respuesta (200):
```json
{
  "fiestas": [
    {
      "id": 1,
      "nombre": "Rave en Finca La Neblina",
      "descripcion": "Open air techno con sonido en la montaña.",
      "ubicacion_texto": "Finca La Neblina, Cartago",
      "latitud": 9.8644,
      "longitud": -83.9194,
      "capacidad_max": 80,
      "fecha": "2026-06-14T22:00:00+00:00",
      "host": "DJ Volcán"
    }
  ]
}
```

### Crear una fiesta

```bash
curl -X POST http://localhost:8000/api/fiestas \
  -H "Content-Type: application/json" \
  -d "{\"nombre\": \"Rave en la montaña\", \"ubicacion_texto\": \"Finca La Neblina, Cartago\", \"latitud\": 9.8644, \"longitud\": -83.9194, \"capacidad_max\": 80, \"fecha\": \"2026-12-14T22:00:00Z\", \"host\": \"DJ Volcán\"}"
```

Respuesta (201):
```json
{
  "id": 5,
  "nombre": "Rave en la montaña",
  "ubicacion_texto": "Finca La Neblina, Cartago",
  "latitud": 9.8644,
  "longitud": -83.9194,
  "capacidad_max": 80,
  "fecha": "2026-12-14T22:00:00+00:00",
  "host": "DJ Volcán"
}
```

### Aceptar una invitación

```bash
curl -X POST http://localhost:8000/api/invitados/1/aceptar
```

Respuesta (200):
```json
{"id": 1, "nombre": "Ana Rojas", "contacto": "ana@example.com", "estado": "accepted", "fiesta_id": 1}
```

Respuesta si la fiesta está llena (409):
```json
{"error": "Fiesta 'Rave en Finca La Neblina' está llena (80/80)"}
```

### Rechazar una invitación

```bash
curl -X POST http://localhost:8000/api/invitados/3/rechazar
```

Respuesta (200):
```json
{"id": 3, "nombre": "Carla Mora", "contacto": "carla@example.com", "estado": "declined", "fiesta_id": 2}
```

---

## Modelo de datos

```
Fiesta
  id               int PK (autoincrement)
  nombre           string (max 200)
  descripcion      text (puede estar vacío)
  ubicacion_texto  string (max 300)     ej: "Finca La Neblina, Cartago"
  latitud          float                rango: [-90, 90]
  longitud         float                rango: [-180, 180]
  capacidad_max    int positivo
  fecha            datetime con timezone
  host             string (max 200)
  created_at       datetime (auto)

Invitado
  id         int PK (autoincrement)
  fiesta     FK → Fiesta (cascade delete)
  nombre     string (max 200)
  contacto   string (max 200, puede estar vacío)
  estado     string: "pending" | "accepted" | "declined" (default: pending)
  created_at datetime (auto)
```

## Reglas de negocio

1. Una fiesta no puede tener más invitados con `estado=accepted` que su `capacidad_max`.
2. Un invitado solo puede cambiar de estado si actualmente está en `pending`.
3. `GET /api/fiestas` y el frontend de localización solo muestran fiestas con `fecha >= ahora`.
4. `nombre`, `ubicacion_texto` y `host` no pueden estar vacíos ni ser solo espacios.
5. `latitud` debe estar en `[-90, 90]`, `longitud` en `[-180, 180]`.
6. `capacidad_max` debe ser un entero positivo (> 0).

---

## Capas y separación de responsabilidades

```
views (api, invitados, localizacion)
  │  solo importan: services, exceptions
  │  NO importan: repositories, models
  ▼
services (fiesta_service, invitado_service)
  │  solo importan: repositories, exceptions
  │  NO importan: models directamente
  ▼
repositories (fiesta_repository, invitado_repository)
  │  solo importan: models (Django ORM)
  │  NO importan: nada de capas superiores
  ▼
models (Fiesta, Invitado)
  │  solo usa Django ORM
  ▼
SQLite (db.sqlite3)
```

Si se migra de SQLite a Postgres (o a un API externo), solo se reescriben los
archivos en `repositories/`. Las capas superiores no cambian.

---

## Estructura del proyecto

```
FiestasClandestinas/
├── manage.py                        # entry point Django
├── requirements.txt                 # solo Django>=5.2
├── .gitignore
│
├── fiestas_project/                 # configuración del proyecto Django
│   ├── settings.py                  #   DJANGO_BUNDLE switch + apps
│   ├── urls.py                      #   monolito completo (BUNDLE=all)
│   ├── urls_api.py                  #   solo REST (BUNDLE=api)
│   ├── urls_invitados.py            #   solo invitados (BUNDLE=invitados)
│   ├── urls_localizacion.py         #   solo localización (BUNDLE=localizacion)
│   ├── wsgi.py
│   └── asgi.py
│
├── fiestas_core/                    # dominio: modelos + repos + servicios
│   ├── models.py                    #   Fiesta, Invitado
│   ├── exceptions.py                #   DomainError, ValidationError, etc.
│   ├── repositories/
│   │   ├── fiesta_repository.py     #   queries Fiesta
│   │   └── invitado_repository.py   #   queries Invitado
│   ├── services/
│   │   ├── fiesta_service.py        #   lógica: crear, listar, cupos
│   │   └── invitado_service.py      #   lógica: registrar, aceptar, rechazar
│   ├── admin.py                     #   registro en Django admin
│   ├── fixtures/
│   │   └── seed.json                #   4 fiestas + 5 invitados
│   └── migrations/
│       └── 0001_initial.py
│
├── apps/
│   ├── api/                         # app: REST endpoints
│   │   ├── views.py                 #   fiestas_collection, invitado_aceptar/rechazar
│   │   ├── serializers.py           #   fiesta_to_dict, invitado_to_dict
│   │   └── urls.py                  #   /api/fiestas, /api/invitados/<id>/...
│   │
│   ├── invitados/                   # app: frontend SSR invitaciones
│   │   ├── views.py                 #   listar, aceptar, rechazar (redirect)
│   │   ├── urls.py                  #   /invitados/...
│   │   └── templates/invitados/
│   │       ├── base.html            #   layout dark neon
│   │       └── list.html            #   cards con Aceptar/Rechazar
│   │
│   └── localizacion/                # app: frontend SSR ubicaciones
│       ├── views.py                 #   listar, detalle
│       ├── urls.py                  #   /localizacion/...
│       └── templates/localizacion/
│           ├── base.html            #   layout terminal verde
│           ├── list.html            #   panels con coords + link OSM
│           └── detail.html          #   detalle de una fiesta
│
├── scripts/                         # runners por bundle
│   ├── run_all.sh / .bat
│   ├── run_api.sh / .bat
│   ├── run_invitados.sh / .bat
│   ├── run_localizacion.sh / .bat
│   └── seed.sh / .bat               #   migrate + loaddata
│
├── tests/                           # 34 smoke tests
│   ├── test_fiesta_service.py       #   7 tests: crear, validar, listar, cupos
│   ├── test_invitado_service.py     #   7 tests: registrar, aceptar, rechazar, capacidad
│   ├── test_api_fiestas.py          #   10 tests: POST/GET, errores, accept/reject
│   ├── test_frontend_invitados.py   #   5 tests: render, form submit, redirect
│   └── test_frontend_localizacion.py #  5 tests: render, coords, detalle, 404
│
├── PLAN.md                          # plan de implementación
├── AGENTS.md                        # agentes de IA usados
└── GIT_FLOW.md                      # política de branches
```

---

## Datos del seed

El archivo `fiestas_core/fixtures/seed.json` carga:

| Fiesta | Ubicación | Capacidad | Fecha | Host |
|---|---|---|---|---|
| Rave en Finca La Neblina | Cartago | 80 | 2026-06-14 22:00 | DJ Volcán |
| Casa Abandonada — noche deep house | Barrio Amón, San José | 30 | 2026-05-02 23:30 | Colectivo Subsuelo |
| Bodega del Puerto | Zona portuaria, Puntarenas | 120 | 2026-07-20 21:00 | Low End Crew |
| Finca del Lago | La Fortuna, Alajuela | 50 | 2026-08-09 17:00 | Luna Colectivo |

| Invitado | Fiesta | Estado |
|---|---|---|
| Ana Rojas | Rave en Finca La Neblina | pending |
| Bruno Vega | Rave en Finca La Neblina | accepted |
| Carla Mora | Casa Abandonada | pending |
| Diego Alfaro | Bodega del Puerto | pending |
| Elena Soto | Finca del Lago | declined |

Para resetear los datos a su estado inicial:
```bash
python manage.py flush --no-input
python manage.py loaddata seed.json
```

---

## Resumen de tecnologías

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.11+ |
| Framework | Django 5.2 |
| Base de datos | SQLite (archivo local `db.sqlite3`) |
| Frontend | Templates Django (SSR, sin JavaScript) |
| CSS | Inline en templates (sin bundler, sin CDN) |
| API | Django views con `JsonResponse` (sin DRF) |
| Tests | `django.test.TestCase` nativo |
| Servidor | `manage.py runserver` (dev server integrado) |

---

## Documentos adicionales

| Documento | Contenido |
|---|---|
| [`PLAN.md`](PLAN.md) | Plan de implementación: fases, modelo de datos, decisiones de diseño |
| [`AGENTS.md`](AGENTS.md) | Agentes de IA especializados usados y en qué fase de desarrollo |
| [`GIT_FLOW.md`](GIT_FLOW.md) | Política de branches, convenciones de commit, checklist pre-merge |

---

## Troubleshooting

**`python` no se encuentra:**
En algunos sistemas el comando es `python3` en vez de `python`. Probar:
```bash
python3 --version
```
Si funciona, usar `python3` en todos los comandos.

**`pip install` falla con permisos:**
Asegurarse de que el virtualenv está activado (el prompt debe mostrar `(.venv)`).

**`loaddata` dice "No fixture named 'seed' found":**
Verificar que estás en la carpeta `FiestasClandestinas/` (donde está `manage.py`).
El archivo es `fiestas_core/fixtures/seed.json` y Django lo busca automáticamente.

**El frontend muestra "Sin invitaciones pendientes":**
Los datos del seed pudieron haber sido modificados por uso previo. Resetear:
```bash
python manage.py flush --no-input
python manage.py loaddata seed.json
```

**`DJANGO_BUNDLE=api python manage.py runserver` no funciona en Windows:**
En Windows CMD usar dos comandos separados:
```cmd
set DJANGO_BUNDLE=api
python manage.py runserver 8000
```
En Windows PowerShell:
```powershell
$env:DJANGO_BUNDLE="api"; python manage.py runserver 8000
```
