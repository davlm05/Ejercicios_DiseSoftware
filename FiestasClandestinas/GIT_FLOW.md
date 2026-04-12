# GIT_FLOW.md — Flujo de branches para el ejercicio

> Responsable: Jose Isaac Corrales Cascante
> Ejercicio 5 · Fiestas Clandestinas

## 1. Política

Este ejercicio se desarrolla usando un **flow de 3 niveles**: `main` → branch de ejercicio → feature branches. No se commitea nunca directamente a `main`, ni a la branch del ejercicio. Todo cambio entra por una feature branch y sube mediante merge.

```
main
 │
 └── ejercicio-5-fiestas-clandestinas        ← branch de integración del ejercicio
      │
      ├── feature/docs-and-plan               ← PLAN.md, AGENTS.md, GIT_FLOW.md
      ├── feature/backend-core                ← models, repositories, services, migraciones, seed
      ├── feature/api-fiestas                 ← POST /api/fiestas, GET /api/fiestas
      ├── feature/frontend-invitados          ← templates + views SSR de invitados
      ├── feature/frontend-localizacion       ← templates + views SSR de localización
      ├── feature/bundles-scripts             ← switch DJANGO_BUNDLE + scripts/
      └── feature/readme-final                ← README.md de presentación
```

## 2. Convención de nombres

| Tipo | Patrón | Ejemplo |
|---|---|---|
| Ejercicio | `ejercicio-<n>-<slug>` | `ejercicio-5-fiestas-clandestinas` |
| Feature | `feature/<slug>` | `feature/api-fiestas` |
| Fix dentro de una feature abierta | commit en la misma feature | — |
| Hotfix a la branch del ejercicio | `fix/<slug>` | `fix/seed-capacidad` |

Los slugs van en kebab-case, en minúsculas, en inglés o español pero consistentes dentro del ejercicio.

## 3. Reglas

1. **Nunca commitear directo a `main`.** `main` solo recibe merges de branches de ejercicio, y solo con aprobación explícita.
2. **Nunca commitear directo a la branch de ejercicio.** Esa branch solo recibe merges de feature branches.
3. **Una feature branch por fase** de `PLAN.md`. Si una fase crece, se puede partir en varias, pero no se mezclan dos fases distintas en la misma branch.
4. **Merges `--no-ff`** hacia la branch del ejercicio, para que el historial muestre cada feature como una unidad.
5. **Commits sin co-autor de IA.** Los mensajes no incluyen `Co-Authored-By: Claude` ni similares (ver `AGENTS.md` para el contexto del uso de agentes).
6. **Mensajes de commit** en español o inglés, imperativo, con prefijo por área:
   - `plan: ...`, `backend: ...`, `api: ...`, `invitados: ...`, `localizacion: ...`, `scripts: ...`, `docs: ...`

## 4. Comandos de referencia

### Arrancar el ejercicio desde main

```bash
git checkout main
git pull
git checkout -b ejercicio-5-fiestas-clandestinas
```

### Abrir una feature branch

```bash
git checkout ejercicio-5-fiestas-clandestinas
git checkout -b feature/<slug>
# ...trabajar...
git add <archivos>
git commit -m "<prefijo>: <mensaje>"
```

### Cerrar una feature → branch del ejercicio

```bash
git checkout ejercicio-5-fiestas-clandestinas
git merge --no-ff feature/<slug> -m "merge: feature/<slug>"
git branch -d feature/<slug>    # opcional, borrar local
```

### Cerrar el ejercicio → main (solo al final, con aprobación)

```bash
git checkout main
git pull
git merge --no-ff ejercicio-5-fiestas-clandestinas -m "merge: ejercicio 5 — fiestas clandestinas"
git push origin main
# opcional: git branch -d ejercicio-5-fiestas-clandestinas
```

## 5. Orden esperado de merges

El orden importa porque las features posteriores dependen de las anteriores:

1. `feature/docs-and-plan` → ejercicio
2. `feature/backend-core` → ejercicio
3. `feature/api-fiestas` → ejercicio
4. `feature/frontend-invitados` → ejercicio
5. `feature/frontend-localizacion` → ejercicio
6. `feature/bundles-scripts` → ejercicio
7. `feature/readme-final` → ejercicio
8. `ejercicio-5-fiestas-clandestinas` → `main` ← **solo aquí y con aprobación explícita**

Si alguna feature se basa en una previa aún no mergeada, se rebasa sobre la branch del ejercicio antes de mergear: `git rebase ejercicio-5-fiestas-clandestinas`.

## 6. Qué revisar antes de mergear a `main`

- [ ] Todas las features cerradas y mergeadas a `ejercicio-5-fiestas-clandestinas`.
- [ ] `README.md` de presentación completo y con instrucciones de cómo correr cada bundle.
- [ ] SQLite con seed reproducible (`python manage.py loaddata fiestas_core/fixtures/seed.json`).
- [ ] Los tres scripts (`run_api`, `run_invitados`, `run_localizacion`) arrancan sin error.
- [ ] `PLAN.md`, `AGENTS.md`, `GIT_FLOW.md` presentes y coherentes con el código final.
- [ ] Historial de commits limpio, sin trailers de co-autoría de IA.
