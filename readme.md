# Proyecto Autolavado

Sistema CRUD de gestión de vehículos y servicios de autolavado, desarrollado como proyecto académico.

## Integrantes del Grupo

| Nombre | Responsabilidad |
|--------|----------------|
| Santiago Garzón Silva (Líder del proyecto) | Backend - Azure App Service |
| Mateo Enrique Bermejo Ramírez | Frontend - Azure Static Web Apps |
| Jonathan Pedroza Bernal | Base de datos - GCP Cloud SQL |

## Descripción del Proyecto y Dominio

Sistema web para la gestión de un autolavado, que permite registrar vehículos y servicios mediante operaciones CRUD. El dominio elegido es la administración de servicios de lavado automotriz.

## Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| Backend | FastAPI (Python 3.11) |
| Base de datos | PostgreSQL 15 (GCP Cloud SQL) |
| Frontend | HTML / CSS / JavaScript |
| Despliegue Backend | Azure App Service |
| Despliegue Frontend | Azure Static Web Apps |
| CI/CD | GitHub Actions |

## Servicios Cloud Implementados

- **GCP Cloud SQL**: Instancia PostgreSQL 15 (`autolavado-db`) en `us-central1`
- **Azure App Service**: Hosting del backend FastAPI (`autolavado-api`)
- **Azure Static Web Apps**: Hosting del frontend estático

## URLs de Acceso a la Aplicación Desplegada

- **Repositorio**: [https://github.com/Closure03/Autolavado](https://github.com/Closure03/Autolavado)
- **Frontend**: *(pendiente por desplegar)*
- **Backend API**: *(pendiente por desplegar)*
- **Documentación API (Swagger)**: *(pendiente por desplegar)*

## Diagrama de Arquitectura del Sistema
```
┌─────────────────────────────────────────────────────────┐
│                        CLIENTE                          │
│              (Navegador Web - HTML/CSS/JS)              │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP/HTTPS
                      ▼
┌─────────────────────────────────────────────────────────┐
│              AZURE STATIC WEB APPS                      │
│                  (Frontend)                             │
└─────────────────────┬───────────────────────────────────┘
                      │ REST API
                      ▼
┌─────────────────────────────────────────────────────────┐
│              AZURE APP SERVICE                          │
│           FastAPI (Python 3.11)                         │
│         autolavado-api.azurewebsites.net                │
└─────────────────────┬───────────────────────────────────┘
                      │ PostgreSQL (puerto 5432)
                      ▼
┌─────────────────────────────────────────────────────────┐
│              GCP CLOUD SQL                              │
│         PostgreSQL 15 - autolavado-db                   │
│              us-central1 (Iowa)                         │
└─────────────────────────────────────────────────────────┘
```

## Instrucciones de Instalación Local

### Prerrequisitos
- Python 3.11+
- PostgreSQL instalado localmente o acceso a GCP Cloud SQL
- Git

### Pasos

1. Clona el repositorio:
```bash
git clone https://github.com/Closure03/Autolavado.git
cd Autolavado
```

2. Crea el entorno virtual e instala dependencias:
```bash
cd backend
python -m venv antenv
source antenv/bin/activate  # En Windows: antenv\Scripts\activate
pip install -r requirements.txt
```

3. Crea el archivo `.env` en `backend/`:
```bash
cp .env.example .env
```

4. Configura la variable de entorno:
```env
DATABASE_URL=postgresql://autolavado_user:PASSWORD@<IP_CLOUD_SQL>:5432/autolavado_db
```

5. Ejecuta los scripts de base de datos:
```bash
psql -h <IP_CLOUD_SQL> -U autolavado_user -d autolavado_db -f database/schema.sql
psql -h <IP_CLOUD_SQL> -U autolavado_user -d autolavado_db -f database/seed.sql
```

## Comandos de Despliegue

### Backend (Azure App Service)
El despliegue es automático via GitHub Actions al hacer push a `master`:
```bash
git add .
git commit -m "mensaje"
git push origin master
```

### Ejecución local:
```bash
cd backend
uvicorn src.main:app --reload
```

## API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/vehiculos` | Lista todos los vehículos |
| POST | `/api/vehiculos` | Crear un vehículo |
| GET | `/api/vehiculos/{id}` | Obtener vehículo por ID |
| PUT | `/api/vehiculos/{id}` | Actualizar vehículo |
| DELETE | `/api/vehiculos/{id}` | Eliminar vehículo |
| GET | `/api/servicios` | Lista todos los servicios |
| POST | `/api/servicios` | Crear un servicio |
| GET | `/api/servicios/{id}` | Obtener servicio por ID |
| PUT | `/api/servicios/{id}` | Actualizar servicio |
| DELETE | `/api/servicios/{id}` | Eliminar servicio |

## Credenciales de Prueba

| Campo | Valor |
|-------|-------|
| Usuario BD | `autolavado_user` |
| Base de datos | `autolavado_db` |
| Puerto | `5432` |
| Host | `<IP_PUBLICA_GCP>` |

> ⚠️ La contraseña y la IP real se comparten de forma privada con el docente.

## Esquema de Base de Datos

Ejecuta los scripts en `backend/database/`:
- `schema.sql`: Crea las tablas (`vehiculos`, `servicios`)
- `seed.sql`: Inserta datos de ejemplo (10 vehículos, 12 servicios)

## Problemas Encontrados y Soluciones

| Problema | Solución |
|----------|----------|
| `Site Disabled (CODE: 403)` en GitHub Actions | Iniciar el App Service desde Azure Portal |
| `Node.js 20 actions are deprecated` | Agregar `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true` en el workflow |
| Tablas no existían al ejecutar schema.sql | Normal — el `DROP TABLE IF EXISTS` lo omite si no existen |

## Capturas de Pantalla

> 📷 *(Pendiente — agregar capturas del frontend funcionando, API Swagger, y base de datos)*

## Configuración de la Base de Datos

### Producción (Azure App Service)
1. En Azure Portal ve a tu App Service → Configuración → Variables de entorno
2. Agrega `DATABASE_URL` con la URL de conexión a GCP Cloud SQL
3. Asegúrate de que la IP de Azure esté autorizada en GCP SQL → Conexiones → Redes autorizadas

### Esquema
```bash
# Conectar via Cloud Shell de GCP
gcloud sql connect autolavado-db --user=autolavado_user --database=autolavado_db

# Ejecutar scripts
\i /ruta/database/schema.sql
\i /ruta/database/seed.sql

# Verificar
SELECT COUNT(*) FROM vehiculos;  -- debe retornar 10
SELECT COUNT(*) FROM servicios;  -- debe retornar 12
```