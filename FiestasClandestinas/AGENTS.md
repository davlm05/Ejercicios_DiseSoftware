# AGENTS.md — Agentes de IA usados en este ejercicio

> El enunciado exige que el código sea generado por agentes de IA especializados. Este documento describe qué agentes se usaron, en qué fase, y con qué responsabilidad.

## 1. Contexto

Todo el código de `FiestasClandestinas/` fue generado asistido por **Claude Code (Anthropic)**, modelo `claude-opus-4-6` (Opus 4.6, ventana de 1M tokens), corriendo como CLI agent en Windows 11. El agente principal delega a sub-agentes especializados para tareas que se benefician de contexto aislado o de expertise específico.

## 2. Agente orquestador

**Rol:** Claude Code (Opus 4.6) como agente principal en el shell del proyecto.

**Responsabilidades:**
- Leer el enunciado y alinear con el usuario los puntos ambiguos **antes** de escribir código.
- Diseñar la arquitectura en capas (ver `PLAN.md`).
- Controlar el git flow: crear la branch de ejercicio, sacar feature branches, mergear, documentar.
- Invocar sub-agentes cuando la tarea lo amerite.
- Revisar el código resultante contra las reglas del proyecto (no co-author, no emojis innecesarios, capas respetadas).

**Restricciones auto-impuestas (feedback del usuario):**
- Nunca firmar commits con `Co-Authored-By: Claude`.
- Nunca commitear directo a `main`.
- Seguir siempre el flow: `main → ejercicio → feature → merge up`.

## 3. Sub-agentes especializados

Los siguientes agentes se invocan bajo demanda desde el orquestador.

### 3.1 `Plan`
- **Cuándo:** al inicio del ejercicio y antes de cada fase no trivial.
- **Por qué:** diseñar la estrategia de implementación sin tocar código, validar trade-offs de topología y de la separación en capas.
- **Entregable típico:** un plan paso a paso y lista de archivos críticos.

### 3.2 `Explore`
- **Cuándo:** antes de modificar código existente o cuando hay que buscar convenciones ya usadas en los ejercicios hermanos (`AmanteIdeal`, `MiMotoMiPasion`).
- **Por qué:** búsquedas amplias sobre el monorepo se delegan al sub-agente para no llenar el contexto principal con resultados de grep.
- **Modo:** `quick` para lookups puntuales, `medium` cuando hay que correlacionar varios archivos.

### 3.3 `database-architect`
- **Cuándo:** en `feature/backend-core`, al diseñar el esquema `Fiesta` / `Invitado` y definir los índices y constraints.
- **Por qué:** valida que el modelado tolere las reglas de negocio (capacidad máxima, fiestas disponibles por fecha) sin meter lógica en la capa de datos.
- **Entregable:** `fiestas_core/models.py` y migraciones iniciales.

### 3.4 `fullstack-developer`
- **Cuándo:** en `feature/api-fiestas`, `feature/frontend-invitados` y `feature/frontend-localizacion`, donde la tarea cruza model → repository → service → view → template.
- **Por qué:** estas features tocan las tres capas del monolito y un solo agente con visión end-to-end evita que las capas se desincronicen.
- **Entregable:** el flujo completo de una feature, tipos y contratos consistentes entre capas.

### 3.5 `frontend-design`
- **Cuándo:** en `feature/frontend-invitados` y `feature/frontend-localizacion`, para los templates HTML/CSS SSR.
- **Por qué:** aunque son templates Django puros (sin SPA ni bundler JS), la presentación importa para la revisión por videollamada. Este agente produce layouts legibles y distintos entre sí para que los dos frontends se vean como productos distintos.
- **Restricción:** todo CSS debe servirse con `{% static %}`, nada de CDN externos.

### 3.6 `test-engineer`
- **Cuándo:** al cerrar cada feature branch, para agregar smoke tests mínimos.
- **Por qué:** el requisito académico no pide coverage, pero queremos al menos un test por service y por endpoint para defender decisiones en la revisión.
- **Alcance:** solo tests en `tests/` con `pytest-django` o `TestCase` nativo de Django.

### 3.7 `documentation-expert`
- **Cuándo:** en `feature/readme-final`, para el README de presentación.
- **Por qué:** el enunciado dice explícitamente que se revisarán los markdown files. Este agente escribe el README con diagramas ASCII, tabla de scripts, y explicación de la topología para un revisor que llega frío.

## 4. Flujo típico de interacción

1. Usuario pide una fase (ej. "hagamos `feature/api-fiestas`").
2. Orquestador crea la feature branch desde `ejercicio-5-fiestas-clandestinas`.
3. Orquestador invoca `Plan` para diseñar los cambios puntuales de esa fase.
4. Orquestador delega la implementación a `fullstack-developer` (o al agente que corresponda).
5. Orquestador revisa el diff, aplica correcciones manuales si hacen falta, invoca `test-engineer` para añadir smoke tests.
6. Commit (sin co-author), push, y se solicita al usuario aprobación para mergear la feature a la branch del ejercicio.
7. Al terminar todas las fases, merge final a `main` solo con confirmación explícita.

## 5. Por qué este setup

La consigna del profesor es que el código sea generado por **AI especializada en coding**. La elección de delegar en sub-agentes por área (DB, fullstack, frontend, tests, docs) en lugar de pedirle todo a un único modelo persigue dos cosas:

1. **Separación de responsabilidades** — el sub-agente entra con un prompt acotado y un contexto limpio, así produce código más coherente con su especialidad.
2. **Auditoría** — al quedar registrado qué agente hizo qué fase, la revisión académica puede entender la trazabilidad del código generado.

El modelo base es el mismo (Opus 4.6), lo que varía es el **prompt del sistema** y las **herramientas disponibles** de cada sub-agente.
