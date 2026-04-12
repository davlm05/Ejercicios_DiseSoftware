# Ejercicio 6 - Lanchas Sin Permisos

Sistema distribuido de microservicios con Micronaut para que guias locales de la comunidad (sin permisos oficiales de turismo) publiquen tours en lanchas y usuarios puedan consultarlos.

## Requisitos previos

- **Java 21** (OpenJDK o similar)
- **Node.js 18+** (con npm)
- **Git**

Verificar instalacion:

```bash
java -version    # debe mostrar 21.x
node -v          # debe mostrar 18.x o superior
npm -v           # incluido con Node.js
```

> No se necesita instalar Gradle. Cada microservicio incluye su propio Gradle Wrapper (`gradlew`).

## Estructura del monorepo

```
LanchasSinPermisos/
├── tours-service/          # Microservicio REST - tours en lancha (puerto 8081)
│   ├── build.gradle
│   ├── gradlew / gradlew.bat
│   └── src/main/java/com/lanchas/tours/
│       ├── Application.java
│       ├── controller/TourController.java
│       ├── service/TourService.java
│       ├── repository/TourRepository.java
│       └── model/Tour.java
├── guides-service/         # Microservicio REST - guias locales (puerto 8082)
│   ├── build.gradle
│   ├── gradlew / gradlew.bat
│   └── src/main/java/com/lanchas/guides/
│       ├── Application.java
│       ├── controller/GuideController.java
│       ├── service/GuideService.java
│       ├── repository/GuideRepository.java
│       └── model/Guide.java
├── frontend/               # React + Tailwind CSS (puerto 5173)
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── api.js
│       └── components/
│           ├── TourForm.jsx
│           ├── TourList.jsx
│           ├── GuideForm.jsx
│           └── GuideList.jsx
├── scripts/                # Scripts de ejecucion dev y prod
├── CLAUDE.md               # Documentacion del agente de IA
├── GIT_FLOW.md             # Flujo de branches
└── README.md               # Este archivo
```

## Como ejecutar (paso a paso)

### Opcion A: Cada servicio en su propia terminal (recomendado)

Abrir 3 terminales y ejecutar desde la carpeta `LanchasSinPermisos/`:

**Terminal 1 - tours-service:**

```bash
cd tours-service
./gradlew run
```

Esperar hasta ver `Startup completed` en la consola. El servicio queda en http://localhost:8081

**Terminal 2 - guides-service:**

```bash
cd guides-service
./gradlew run
```

Esperar hasta ver `Startup completed`. El servicio queda en http://localhost:8082

**Terminal 3 - frontend:**

```bash
cd frontend
npm install
npm run dev
```

Abrir http://localhost:5173 en el navegador.

> **IMPORTANTE:** El frontend DEBE correr en el puerto 5173. Si ese puerto esta ocupado, los microservicios rechazaran las peticiones por CORS. Si el puerto esta ocupado, matar el proceso que lo usa antes de iniciar.

### Opcion B: Scripts individuales

```bash
bash scripts/dev-tours.sh      # Terminal 1
bash scripts/dev-guides.sh     # Terminal 2
bash scripts/dev-frontend.sh   # Terminal 3
```

### Opcion C: Todo junto

```bash
bash scripts/dev-all.sh
```

Ctrl+C para detener todo.

### En Windows (cmd o PowerShell)

Usar `gradlew.bat` en lugar de `./gradlew`:

```cmd
cd tours-service
gradlew.bat run
```

## Probar con curl

Una vez que los servicios esten corriendo:

### Crear un tour

```bash
curl -X POST http://localhost:8081/tours \
  -H "Content-Type: application/json" \
  -d '{"name":"Tour Isla del Cano","location":"Bahia Drake","price":45.0,"guideName":"Carlos Mora","description":"Snorkel en arrecifes","maxCapacity":8}'
```

Respuesta (HTTP 201):
```json
{
  "id": 1,
  "name": "Tour Isla del Cano",
  "location": "Bahia Drake",
  "price": 45.0,
  "guideName": "Carlos Mora",
  "description": "Snorkel en arrecifes",
  "maxCapacity": 8,
  "available": true
}
```

### Listar tours disponibles

```bash
curl http://localhost:8081/tours
```

### Obtener un tour por ID

```bash
curl http://localhost:8081/tours/1
```

### Registrar un guia

```bash
curl -X POST http://localhost:8082/guides \
  -H "Content-Type: application/json" \
  -d '{"name":"Carlos Mora","phone":"8812-3456","zone":"Bahia Drake","experience":5}'
```

### Listar guias activos

```bash
curl http://localhost:8082/guides
```

## Arquitectura

### Paradigma y topologia

- **Framework:** Micronaut 4.x (microservicios JVM)
- **Paradigma:** Microservicios REST independientes
- **Topologia:** Monorepo con servicios aislados, sin codigo compartido
- **Base de datos:** H2 file-based (una por servicio, persistente en `data/`)
- **Migraciones:** Flyway (versionadas en `db/migration/`)
- **Frontend:** React 19 + Tailwind CSS 4 (Vite 8)

### Capas por microservicio

Cada microservicio sigue la misma separacion en capas:

```
controller/    Recibe peticiones HTTP, delega al service
service/       Logica de negocio, validaciones, defaults
repository/    Acceso a datos via Micronaut Data JDBC
model/         Entidades del dominio (@MappedEntity, @Serdeable)
```

### Diagrama de comunicacion

```
                    +-------------------+
                    |     Frontend      |
                    | React + Tailwind  |
                    |   localhost:5173  |
                    +--------+----------+
                             |
              +--------------+--------------+
              |  HTTP (fetch)               |  HTTP (fetch)
              v                             v
   +-------------------+        +-------------------+
   |   tours-service   |        |  guides-service   |
   |   Micronaut REST  |        |  Micronaut REST   |
   |  localhost:8081   |        |  localhost:8082    |
   +--------+----------+        +--------+----------+
            |                             |
            v                             v
   +-------------------+        +-------------------+
   |  H2 (tours-db)    |        |  H2 (guides-db)   |
   |  data/tours-db    |        |  data/guides-db    |
   +-------------------+        +-------------------+
```

### Endpoints

| Servicio | Metodo | Ruta | Descripcion |
|----------|--------|------|-------------|
| tours-service | POST | /tours | Crear tour (name, location, price, guideName) |
| tours-service | GET | /tours | Listar tours disponibles |
| tours-service | GET | /tours/{id} | Obtener tour por ID |
| guides-service | POST | /guides | Registrar guia (name, phone, zone) |
| guides-service | GET | /guides | Listar guias activos |
| guides-service | GET | /guides/{id} | Obtener guia por ID |

## Produccion

Los scripts de produccion compilan un fat JAR con Shadow y lo ejecutan:

```bash
bash scripts/prod-tours.sh      # Compila y ejecuta tours-service
bash scripts/prod-guides.sh     # Compila y ejecuta guides-service
bash scripts/prod-frontend.sh   # Build y preview del frontend
```

## Troubleshooting

| Problema | Solucion |
|----------|---------|
| `Failed to fetch` en el frontend | Verificar que los microservicios esten corriendo en puertos 8081 y 8082 |
| CORS error en consola del browser | El frontend DEBE estar en puerto 5173. Matar procesos que ocupen ese puerto |
| `Port 5173 is in use` | Ejecutar `npx kill-port 5173` o en Windows: `netstat -ano \| findstr :5173` y luego `taskkill /PID <pid> /F` |
| `gradlew: Permission denied` | Ejecutar `chmod +x gradlew` dentro del microservicio |
| Java no encontrado | Instalar OpenJDK 21 y verificar con `java -version` |

## Integrantes

- Isaac Corrales
- David Lopez
