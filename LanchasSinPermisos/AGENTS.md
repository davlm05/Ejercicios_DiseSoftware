# AGENTS.md — Agentes de IA usados en este ejercicio

> El enunciado exige que el código sea generado por agentes de IA especializados. Este documento describe qué agentes se usaron, en qué fase, y con qué responsabilidad.

## 1. Contexto

Todo el código de `LanchasSinPermisos/` fue generado asistido por **Claude Code (Anthropic)**, modelo `claude-opus-4-6` (Opus 4.6, ventana de 1M tokens), corriendo como CLI agent en Windows 11. El agente principal delega a sub-agentes especializados para tareas que se benefician de contexto aislado o de expertise específico.

## 2. Agente orquestador

**Rol:** Claude Code (Opus 4.6) como agente principal en el shell del proyecto.

**Responsabilidades:**
- Leer el enunciado y alinear con el usuario los requisitos de microservicios.
- Diseñar la topología distribuida (ver `PLAN.md`).
- Controlar el git flow: crear la branch de ejercicio, sacar feature branches, mergear, documentar.
- Invocar sub-agentes cuando la tarea lo amerite.
- Revisar el código resultante contra las reglas del proyecto (separación estricta entre servicios, capas correctas, CORS configurado).

**Restricciones auto-impuestas:**
- Nunca commitear directo a `main` ni a la branch del ejercicio.
- Seguir el flow: `main → ejercicio → feature → merge up`.
- Verificar que no se comparta código entre microservicios.

## 3. Sub-agentes especializados

Los siguientes agentes se invocan bajo demanda desde el orquestador.

### 3.1 `Plan`
- **Cuándo:** al inicio del ejercicio y antes de cada microservicio.
- **Por qué:** diseñar la topología de microservicios, definir contratos REST entre frontend y backends, validar que la separación sea real y no solo cosmética.
- **Entregable típico:** plan paso a paso, lista de endpoints, esquema de datos por servicio.

### 3.2 `Explore`
- **Cuándo:** antes de modificar código existente o cuando hay que buscar convenciones ya usadas en los ejercicios hermanos (`FiestasClandestinas`, `AmanteIdeal`, etc.).
- **Por qué:** búsquedas amplias sobre el monorepo se delegan al sub-agente para no llenar el contexto principal con resultados de grep.
- **Modo:** `quick` para lookups puntuales, `very thorough` para auditorías completas.

### 3.3 `database-architect`
- **Cuándo:** en `feature/tours-service` y `feature/guides-service`, al diseñar las tablas `tour` y `guide`.
- **Por qué:** valida que cada microservicio tenga su propia base de datos independiente, que las migraciones Flyway sean correctas, y que los tipos de datos sean apropiados para H2.
- **Entregable:** migraciones SQL en `db/migration/V1__*.sql` y modelos Java con `@MappedEntity`.

### 3.4 `fullstack-developer`
- **Cuándo:** en `feature/tours-service`, `feature/guides-service` y `feature/frontend`, donde la tarea cruza model → repository → service → controller → React component.
- **Por qué:** cada microservicio necesita sus 4 capas bien conectadas, y el frontend debe consumir ambos servicios con el contrato REST correcto. Un agente con visión end-to-end evita que las capas o los servicios se desincronicen.
- **Entregable:** el flujo completo de cada microservicio y los componentes React correspondientes.

### 3.5 `frontend-design`
- **Cuándo:** en `feature/frontend`, para los componentes React con Tailwind CSS.
- **Por qué:** la UI necesita ser clara y funcional para la revisión por videollamada. Dos secciones visualmente distintas (tours con tema sky/azul, guías con tema emerald/verde) para que se note la separación de dominios.
- **Entregable:** componentes React con Tailwind, dark theme, tabs de navegación.

### 3.6 `documentation-expert`
- **Cuándo:** en `feature/readme-final`, para el README de presentación.
- **Por qué:** el enunciado dice que se revisarán los markdown files. Este agente escribe el README con diagramas ASCII, tablas de endpoints, y explicación de la topología para un revisor que llega frío.
- **Entregable:** `README.md`, `PLAN.md`, `AGENTS.md`, `GIT_FLOW.md`.

## 4. Flujo típico de interacción

1. Usuario pide una fase (ej. "hagamos `feature/tours-service`").
2. Orquestador crea la feature branch desde `ejercicio-6-lanchas-sin-permisos`.
3. Orquestador invoca `Plan` para diseñar los cambios puntuales de esa fase.
4. Orquestador delega la implementación a `fullstack-developer` (o al agente que corresponda).
5. Orquestador revisa el diff, aplica correcciones si hacen falta.
6. Commit, push, y se solicita al usuario aprobación para mergear la feature a la branch del ejercicio.
7. Al terminar todas las fases, merge final a `main` solo con confirmación explícita.

## 5. Por qué este setup

La consigna del profesor es que el código sea generado por **AI especializada en coding**. La elección de delegar en sub-agentes por área (DB, fullstack, frontend, docs) en lugar de pedirle todo a un único modelo persigue dos cosas:

1. **Separación de responsabilidades** — el sub-agente entra con un prompt acotado y un contexto limpio, así produce código más coherente con su especialidad.
2. **Auditoría** — al quedar registrado qué agente hizo qué fase, la revisión académica puede entender la trazabilidad del código generado.

El modelo base es el mismo (Opus 4.6), lo que varía es el **prompt del sistema** y las **herramientas disponibles** de cada sub-agente.
