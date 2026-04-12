# Plan de Implementación — Lanchas Sin Permisos

> Ejercicio 6 · Diseño de Software · TEC 2026
> Responsable: Jose Isaac Corrales Cascante

## 1. Objetivo

Construir un **sistema distribuido de microservicios con Micronaut** donde guías
locales de la comunidad (sin permisos oficiales de turismo) publiquen tours en
lanchas y usuarios puedan consultarlos. El sistema vive en un monorepo con
microservicios pequeños, bien aislados y desplegables por separado.

## 2. Topología

```
┌─────────────────────────────────────────────────────────────────┐
│                    Monorepo (un repositorio)                    │
│                                                                 │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐  │
│  │ tours-service   │  │ guides-service  │  │    frontend      │  │
│  │  (Micronaut)    │  │  (Micronaut)    │  │ (React+Tailwind) │  │
│  │   :8081         │  │   :8082         │  │    :5173         │  │
│  │                 │  │                 │  │                  │  │
│  │  ┌───────────┐  │  │  ┌───────────┐  │  │  Consume ambos   │  │
│  │  │ H2 (file) │  │  │  │ H2 (file) │  │  │  via REST        │  │
│  │  └───────────┘  │  │  └───────────┘  │  │                  │  │
│  └────────────────┘  └────────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**Punto clave:** cada microservicio es una aplicación Micronaut independiente
con su propio proceso JVM, su propia base de datos H2, y su propio Gradle build.
No se comparte código entre servicios. El frontend React es una SPA que consume
ambos servicios por HTTP.

## 3. Arquitectura y paradigma

### Paradigma: Microservicios REST

- Cada servicio expone una API REST con endpoints bien definidos.
- No hay comunicación directa entre microservicios — el frontend es el orquestador.
- Cada servicio se puede desplegar, escalar y reiniciar sin afectar al otro.

### Framework: Micronaut 4.x

Micronaut fue elegido sobre Spring Boot por:
- **Startup rápido** — inyección de dependencias en compile-time, no reflection.
- **Bajo consumo de memoria** — ideal para microservicios pequeños.
- **Micronaut Data JDBC** — acceso a datos type-safe con annotation processing.
- **AOT (Ahead of Time)** — optimizaciones en compilación para producción.

### Base de datos: H2 (file-based)

- Cada servicio tiene su propia DB H2 en `./data/{service}-db`.
- Migraciones manejadas por Flyway (versionadas en `db/migration/`).
- H2 corre embebida en el proceso JVM — sin servidor de DB externo.

## 4. Capas por microservicio

Cada microservicio sigue la misma estructura de capas:

| Capa | Responsabilidad | Ubicación |
|------|----------------|-----------|
| `model/` | Entidades del dominio con `@MappedEntity` | `src/main/java/.../model/` |
| `repository/` | Acceso a datos via `CrudRepository` de Micronaut Data | `src/main/java/.../repository/` |
| `service/` | Lógica de negocio: validaciones, valores por defecto, reglas | `src/main/java/.../service/` |
| `controller/` | Endpoints REST: recibe HTTP, delega al service, retorna response | `src/main/java/.../controller/` |

**Regla de dependencia:** controller → service → repository → model.
Nunca en dirección contraria. El controller no toca el repository directamente.

## 5. Modelo de datos

### Tours Service

```sql
CREATE TABLE tour (
    id             BIGINT AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(255) NOT NULL,
    location       VARCHAR(255) NOT NULL,
    price          DOUBLE NOT NULL,
    guide_name     VARCHAR(255) NOT NULL,
    description    VARCHAR(1000),
    max_capacity   INT DEFAULT 10,
    available      BOOLEAN DEFAULT TRUE
);
```

### Guides Service

```sql
CREATE TABLE guide (
    id             BIGINT AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(255) NOT NULL,
    phone          VARCHAR(50) NOT NULL,
    zone           VARCHAR(255) NOT NULL,
    experience     INT DEFAULT 0,
    active         BOOLEAN DEFAULT TRUE
);
```

## 6. API

### Tours Service (puerto 8081)

| Método | Ruta | Body | Response | Capa |
|--------|------|------|----------|------|
| POST | `/tours` | JSON `{name, location, price, guideName, description?, maxCapacity?}` | 201 + tour creado | service.createTour |
| GET | `/tours` | — | 200 + lista de tours disponibles | service.listAvailableTours |
| GET | `/tours/{id}` | — | 200 + tour / 404 | service.findById |

### Guides Service (puerto 8082)

| Método | Ruta | Body | Response | Capa |
|--------|------|------|----------|------|
| POST | `/guides` | JSON `{name, phone, zone, experience?}` | 201 + guía creado | service.createGuide |
| GET | `/guides` | — | 200 + lista de guías activos | service.listActiveGuides |
| GET | `/guides/{id}` | — | 200 + guía / 404 | service.findById |

## 7. Frontend

- **Framework:** React 19 + Vite 8
- **Styling:** Tailwind CSS 4 (via plugin de Vite, sin config file separado)
- **Navegación:** tabs (Tours vs Guides) sin router — SPA de una sola página
- **API client:** `api.js` con `fetch()` a `localhost:8081` y `localhost:8082`

### Componentes

| Componente | Responsabilidad |
|-----------|----------------|
| `App.jsx` | Layout principal, tabs, estado de refresh |
| `TourForm.jsx` | Formulario para crear tours |
| `TourList.jsx` | Lista de tours disponibles |
| `GuideForm.jsx` | Formulario para registrar guías |
| `GuideList.jsx` | Lista de guías activos |

## 8. Scripts

Todos en `scripts/`, ejecutables con `bash scripts/<nombre>.sh`:

| Script | Qué hace |
|--------|----------|
| `dev-tours.sh` | `./gradlew run` en tours-service |
| `dev-guides.sh` | `./gradlew run` en guides-service |
| `dev-frontend.sh` | `npm run dev` en frontend |
| `dev-all.sh` | Arranca los 3 servicios en background |
| `prod-tours.sh` | `./gradlew shadowJar` + `java -jar` (fat JAR) |
| `prod-guides.sh` | `./gradlew shadowJar` + `java -jar` (fat JAR) |
| `prod-frontend.sh` | `npm run build` + `npm run preview` |

## 9. Fases de implementación

| # | Feature branch | Entregable |
|---|---------------|-----------|
| 1 | `feature/docs-and-plan` | `PLAN.md`, `AGENTS.md`, `GIT_FLOW.md` |
| 2 | `feature/tours-service` | Microservicio completo: model, repository, service, controller, migration, application.yml |
| 3 | `feature/guides-service` | Microservicio completo con la misma estructura |
| 4 | `feature/frontend` | React + Tailwind con componentes para tours y guías |
| 5 | `feature/scripts` | Scripts de dev y prod por servicio |
| 6 | `feature/readme-final` | `README.md` de presentación con diagramas y cómo correr |

Cada feature branch mergea a `ejercicio-6-lanchas-sin-permisos`. Al final, esa
branch mergea a `main` (ver `GIT_FLOW.md`).

## 10. Stack y dependencias

### Backend (por microservicio)

- Java 21
- Micronaut 4.x (Netty, Serde, Data JDBC, Flyway, HikariCP)
- H2 Database (embebida, file-based)
- Gradle con Shadow plugin (para fat JAR de producción)

### Frontend

- Node.js 18+
- React 19 + ReactDOM
- Vite 8
- Tailwind CSS 4 (via `@tailwindcss/vite`)
- ESLint

## 11. Qué NO vamos a hacer

- No hay autenticación ni autorización — los endpoints son públicos.
- No hay comunicación entre microservicios (no hay service discovery ni API gateway).
- No hay Docker ni Kubernetes — todo corre localmente.
- No hay tests automatizados más allá de la compilación y validación manual con curl.
- No hay base de datos externa — H2 embebida es suficiente para el ejercicio.
- No hay paginación ni filtros avanzados en los endpoints GET.

## 12. Configuración clave

### CORS

Ambos microservicios tienen CORS habilitado para `http://localhost:5173` en su
`application.yml`, permitiendo que el frontend React haga fetch sin problemas.

### Base de datos separadas

- tours-service: `jdbc:h2:file:./data/tours-db`
- guides-service: `jdbc:h2:file:./data/guides-db`

Cada servicio crea su directorio `data/` al arrancar si no existe. Las
migraciones Flyway corren automáticamente al startup.
