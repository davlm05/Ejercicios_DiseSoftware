# Mi Moto, Mi Pasion - Serverless API

Este proyecto sirve de ejercicio y plantilla para demostrar el uso de tecnologías Serverless locales para un mercado de partes de motocicletas. 

## Arquitectura y Estructura
- **Serverless Framework**: Gestiona y simula la infraestructura de AWS.
- **Plugins locales**: `serverless-offline` y `serverless-dynamodb`.
- **Base de Datos**: DynamoDB local inicializado en memoria en el puerto 8000.
- **Capas Desacopladas**:
  - `src/model/`: Entidades de dominio.
  - `src/repositories/`: Accesos a datos en DynamoDB usando AWS SDK.
  - `src/business/`: Reglas de negocio.
  - `src/handlers/`: Controladores para interactuar con API Gateway.

## Prerrequisitos
- Node.js (se recomiendan versiones LTS como 18.x)
- Java Runtime Environment (JRE) (requerido para ejecutar el jar de DynamoDB Local)

## Instrucciones de Uso

### 1. Instalación de Dependencias
```bash
npm install
```

### 2. Instalación de DynamoDB Local
*Requiere JAVA instalado en el sistema. Debe ejecutarse solo la primera vez.*
```bash
npm run install-db
```

### 3. Ejecución (Emulación Local)
```bash
npm start
```
*Este comando iniciará DynamoDB, ejecutará las migraciones y "seed" inicial, y levantará el servidor offline en `http://localhost:3000`.*

## Operaciones / Pruebas (cURL)

La base de datos viene pre-cargada con algunas partes de prueba gracias al archivo `seed.json`.

**1. Operación de Lectura (GET /partes?tipo=x)**:
Para listar todas las partes de motos de la categoría "Llantas":
```bash
curl -X GET "http://localhost:3000/partes?tipo=Llantas"
```

**2. Operación de Escritura (POST /partes)**:
Para registrar una nueva batería en la categoría "Electrica":
```bash
curl -X POST "http://localhost:3000/partes" \
     -H "Content-Type: application/json" \
     -d '{
           "nombre": "Bateria LTH YTX9-BS",
           "tipo": "Electrica",
           "precio": 1200.50
         }'
```
