# Proyecto Autolavado

Sistema CRUD de gestión de vehículos y servicios de autolavado.

## Arquitectura
- **Backend**: FastAPI (Python) desplegado en Azure App Service
- **Base de Datos**: GCP Cloud SQL (PostgreSQL)
- **Frontend**: HTML/CSS/JS (desplegado en Azure Static Web Apps)

## Configuración de la Base de Datos

### Credenciales
Las credenciales de la base de datos se configuran mediante la variable de entorno `DATABASE_URL`.

#### Desarrollo
1. Crea un archivo `.env` en la carpeta `backend/` basado en `.env.example`.
2. Instala las dependencias: `pip install -r backend/requirements.txt`
3. Para usar Cloud SQL Auth proxy (recomendado):
   - Descarga e instala el proxy: https://cloud.google.com/sql/docs/postgres/connect-auth-proxy
   - Ejecuta: `cloud_sql_proxy -instances=tu_proyecto:tu_region:tu_instancia=tcp:5432`
   - Configura `DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/base_de_datos`

#### Producción (Azure App Service)
1. En Azure Portal, ve a tu App Service > Configuración > Variables de entorno.
2. Agrega `DATABASE_URL` con la URL de conexión a GCP Cloud SQL.
3. Asegúrate de que la IP de Azure esté autorizada en GCP SQL > Conexiones > Redes autorizadas.

### Esquema de la Base de Datos
Ejecuta los scripts en `backend/database/`:
- `schema.sql`: Crea las tablas
- `seed.sql`: Inserta datos de ejemplo

## Ejecutar el Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## API Endpoints
- GET /api/vehiculos: Lista vehículos
- POST /api/vehiculos: Crear vehículo
- etc. (ver documentación completa en `backend/docs/api-documentation.md`)
