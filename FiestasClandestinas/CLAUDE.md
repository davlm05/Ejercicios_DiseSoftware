# CLAUDE.md — Instrucciones para agentes de IA

Este archivo contiene las instrucciones necesarias para que un agente de IA
(Claude Code, Cursor, Copilot, etc.) pueda ejecutar, modificar y probar este
proyecto sin intervención humana.

## Qué es este proyecto

Monolito Django con SSR para gestionar fiestas clandestinas. Un solo proyecto
Django que expone 3 superficies (API REST, frontend invitados, frontend
localización) seleccionables con la variable de entorno `DJANGO_BUNDLE`.

## Cómo ejecutar desde cero

```bash
cd FiestasClandestinas
python -m venv .venv
# activar según tu OS:
#   Linux/macOS:       source .venv/bin/activate
#   Windows bash:      source .venv/Scripts/activate
#   Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata seed.json
python manage.py runserver 8000
```

Si estás en Windows y no podés usar `source`, invocá el Python del venv
directamente:
```bash
.venv/Scripts/python.exe manage.py migrate
.venv/Scripts/python.exe manage.py loaddata seed.json
.venv/Scripts/python.exe manage.py runserver 8000
```

## Cómo correr tests

```bash
python manage.py test tests -v 1
```

Resultado esperado: 34 tests, todos OK.

## Cómo correr bundles por separado

```bash
DJANGO_BUNDLE=api python manage.py runserver 8000
DJANGO_BUNDLE=invitados python manage.py runserver 8001
DJANGO_BUNDLE=localizacion python manage.py runserver 8002
```

## Arquitectura de capas

```
views → services → repositories → models → SQLite
```

- views (en apps/) solo importan services y exceptions
- services (en fiestas_core/services/) solo importan repositories
- repositories (en fiestas_core/repositories/) son el único punto de acceso al ORM
- models (en fiestas_core/models.py) definen Fiesta e Invitado

Si necesitás agregar un nuevo campo o entidad:
1. Modificar `fiestas_core/models.py`
2. Agregar queries en `fiestas_core/repositories/`
3. Agregar lógica en `fiestas_core/services/`
4. Exponer en `apps/api/views.py` o en los templates SSR
5. Correr `python manage.py makemigrations` y `python manage.py migrate`

## Convenciones

- No usar DRF — la API usa `JsonResponse` pelado
- Los templates son SSR (Django templates), sin JavaScript
- Los CSS van inline en `base.html` de cada app (sin CDN, sin bundler)
- Tests en `tests/` con `django.test.TestCase`
- Fixtures en `fiestas_core/fixtures/seed.json`
- Excepciones de dominio en `fiestas_core/exceptions.py`

## Archivos clave

| Archivo | Para qué |
|---|---|
| `fiestas_project/settings.py` | Config Django + switch DJANGO_BUNDLE |
| `fiestas_core/models.py` | Entidades Fiesta e Invitado |
| `fiestas_core/services/fiesta_service.py` | Lógica de negocio de fiestas |
| `fiestas_core/services/invitado_service.py` | Lógica de negocio de invitados |
| `apps/api/views.py` | Endpoints REST |
| `apps/invitados/views.py` | Vistas SSR de invitaciones |
| `apps/localizacion/views.py` | Vistas SSR de localización |

## Git

- No commitear con `Co-Authored-By: Claude`
- No commitear directo a `main` — usar feature branches
- Mensajes de commit en español o inglés, con prefijo: `backend:`, `api:`, `invitados:`, `localizacion:`, `scripts:`, `docs:`
