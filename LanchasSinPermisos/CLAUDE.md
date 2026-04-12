# Lanchas Sin Permisos

## Descripcion del proyecto
Sistema distribuido de microservicios para que guias locales de la comunidad (sin permisos oficiales de turismo) publiquen tours en lanchas y usuarios puedan consultarlos.

## Arquitectura

### Tecnologia y paradigma
- **Framework**: Micronaut 4.x (JVM microservices framework)
- **Paradigma**: Microservicios REST independientes
- **Topologia**: Monorepo con servicios aislados, cada uno con su propia base de datos
- **Base de datos**: H2 (file-based, una por servicio)
- **Frontend**: React + Tailwind CSS (Vite)
- **Java**: 21

### Microservicios

| Servicio | Puerto | Responsabilidad | Endpoints |
|----------|--------|----------------|-----------|
| tours-service | 8081 | CRUD de tours de lanchas | POST/GET /tours, GET /tours/{id} |
| guides-service | 8082 | CRUD de guias locales | POST/GET /guides, GET /guides/{id} |
| frontend | 5173 | UI React + Tailwind | Consume ambos servicios |

### Capas por microservicio
Cada microservicio sigue la misma estructura de capas:
- `controller/` - Endpoints REST (recibe HTTP, delega al service)
- `service/` - Logica de negocio (validaciones, defaults)
- `repository/` - Acceso a datos (Micronaut Data JDBC)
- `model/` - Entidades del dominio (@MappedEntity)

### Separacion estricta
- No se comparte codigo entre microservicios
- Cada servicio tiene su propio `build.gradle`, `gradlew`, base de datos H2
- Los servicios se comunican unicamente via REST (el frontend consume ambos)

## Estructura del monorepo
```
LanchasSinPermisos/
├── tours-service/       # Microservicio de tours (puerto 8081)
├── guides-service/      # Microservicio de guias (puerto 8082)
├── frontend/            # React + Tailwind (puerto 5173)
├── scripts/             # Scripts de dev y prod por servicio
└── CLAUDE.md
```

## Como ejecutar

### Desarrollo (cada servicio por separado)
```bash
bash scripts/dev-tours.sh      # Terminal 1
bash scripts/dev-guides.sh     # Terminal 2
bash scripts/dev-frontend.sh   # Terminal 3
```

### Desarrollo (todo junto)
```bash
bash scripts/dev-all.sh
```

### Produccion
```bash
bash scripts/prod-tours.sh
bash scripts/prod-guides.sh
bash scripts/prod-frontend.sh
```

## Agente de generacion
Todo el codigo fue generado usando **Claude Code** (Claude Opus) como agente de IA para coding. El proceso fue:

1. **Scaffolding**: Se uso la API de Micronaut Launch para generar los proyectos base con features `data-jdbc`, `h2`, `flyway`
2. **Backend**: Se generaron las capas (model, repository, service, controller) para cada microservicio de forma independiente
3. **Frontend**: Se uso `create-vite` con template React y se agrego Tailwind CSS via `@tailwindcss/vite`
4. **Scripts**: Se generaron scripts bash para dev y prod de cada servicio
5. **Validacion**: Compilacion con `./gradlew build` y pruebas curl para verificar cada microservicio
