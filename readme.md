# 🚗 AutoLavado Cloud — Sistema de Gestión de Vehículos

> Aplicación web full-stack desplegada en infraestructura multi-cloud.
> **Frontend + Backend → Microsoft Azure** | **Base de datos PostgreSQL → Google Cloud Platform**

🌐 **Aplicación en producción:** [https://icy-forest-05be6d20f.2.azurestaticapps.net](https://icy-forest-05be6d20f.2.azurestaticapps.net)

---

## 👥 Integrantes y división de responsabilidades

| Integrante | Rol |
|---|---|
| Santiago Garzón Silva (Líder del proyecto) | Backend: FastAPI, modelos, endpoints REST |
| Mateo Enrique Bermejo Ramírez | Base de datos GCP Cloud SQL, schema, seed |
| Jonathan Pedroza Bernal | Frontend HTML/CSS/JS, despliegue Azure Static Web Apps |

---

## 📋 Descripción del proyecto

Sistema CRUD completo para la gestión de vehículos y servicios de un autolavado. Implementa dos entidades relacionadas:

- **Vehículos** — entidad principal con CRUD completo (placa, marca, modelo, tipo, propietario)
- **Servicios** — historial de lavados asociados a cada vehículo (tipo, precio, estado)

---

## ⚙️ Stack tecnológico

| Capa | Tecnología |
|---|---|
| Backend | FastAPI (Python 3.11) |
| Base de datos | PostgreSQL 15 |
| ORM | SQLAlchemy 2.0 |
| Validación | Pydantic v2 |
| Servidor | Uvicorn |
| Frontend | HTML5 / CSS3 / JavaScript Vanilla |

---

## ☁️ Servicios cloud implementados

| Servicio | Proveedor | Uso |
|---|---|---|
| App Service (B1) | Microsoft Azure | Backend FastAPI |
| Static Web Apps (Free) | Microsoft Azure | Frontend estático |
| Cloud SQL PostgreSQL 15 | Google Cloud Platform | Base de datos |

---

## 🌐 URLs del sistema

| Componente | URL |
|---|---|
| **Frontend** | https://icy-forest-05be6d20f.2.azurestaticapps.net |
| **Backend API** | https://autolavado-api-hka0hhbcfygjawey.canadacentral-01.azurewebsites.net |
| **Swagger UI** | https://autolavado-api-hka0hhbcfygjawey.canadacentral-01.azurewebsites.net/docs |
| **Health check** | https://autolavado-api-hka0hhbcfygjawey.canadacentral-01.azurewebsites.net/ |

---

## 🏗️ Arquitectura del sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                      USUARIO / BROWSER                          │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTTPS
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MICROSOFT AZURE                               │
│                                                                  │
│  ┌──────────────────────────┐                                    │
│  │  Azure Static Web Apps   │  https://icy-forest-...           │
│  │  HTML / CSS / JavaScript │                                    │
│  └────────────┬─────────────┘                                    │
│               │ HTTPS → API REST                                 │
│               ▼                                                  │
│  ┌──────────────────────────┐                                    │
│  │  Azure App Service (B1)  │  autolavado-api-hka0...           │
│  │  FastAPI + Uvicorn       │  Python 3.11                       │
│  │  Startup: cd backend &&  │                                    │
│  │  uvicorn src.main:app    │                                    │
│  └────────────┬─────────────┘                                    │
└───────────────┼─────────────────────────────────────────────────┘
                │ TCP 5432 / SSL
                ▼
┌─────────────────────────────────────────────────────────────────┐
│                  GOOGLE CLOUD PLATFORM                           │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Cloud SQL — PostgreSQL 15                               │   │
│  │  Instancia: autolavado-db  ·  Región: us-central1        │   │
│  │  Base de datos: autolavado_db                            │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Estructura del repositorio

```
Autolavado/
├── .github/
│   └── workflows/
│       ├── azure-static-web-apps-*.yml   # Deploy frontend → Azure Static Web Apps
│       └── master_autolavado-api.yml     # Deploy backend → Azure App Service
├── backend/
│   ├── database/
│   │   ├── schema.sql                    # Creación de tablas DDL
│   │   └── seed.sql                      # Datos de prueba (10 vehículos, 12 servicios)
│   ├── docs/
│   │   ├── api-documentation.md
│   │   ├── deployment-guide.md
│   │   └── screenshots/
│   ├── frontend/
│   │   ├── index.html                    # Interfaz principal
│   │   ├── style.css                     # Estilos (paleta Azure + GCP)
│   │   └── script.js                     # Lógica CRUD + consumo API
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py                       # FastAPI: endpoints REST + CORS
│   │   ├── models.py                     # SQLAlchemy: Vehiculo, Servicio
│   │   ├── schemas.py                    # Pydantic v2: validación
│   │   └── database.py                   # Conexión GCP Cloud SQL
│   ├── .env                              # Variables locales (NO subir a GitHub)
│   ├── requirements.txt                  # Dependencias Python
│   └── test_connection.py                # Script de prueba de conexión DB
├── video/
│   └── sustentacion.mp4
└── readme.md
```

---

## 📡 Endpoints de la API

### Vehículos — CRUD completo

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/vehiculos` | Lista todos los vehículos |
| `GET` | `/api/vehiculos/{id}` | Obtiene un vehículo por ID |
| `POST` | `/api/vehiculos` | Registra un nuevo vehículo |
| `PUT` | `/api/vehiculos/{id}` | Actualiza un vehículo |
| `DELETE` | `/api/vehiculos/{id}` | Elimina un vehículo y sus servicios |

### Servicios

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/servicios` | Lista todos los servicios |
| `POST` | `/api/servicios` | Registra un nuevo servicio |
| `DELETE` | `/api/servicios/{id}` | Elimina un servicio |

### Relación

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/vehiculos/{id}/servicios` | Historial de servicios de un vehículo |

---

## 🚀 Instalación local

### Prerrequisitos

```
Python 3.11+
PostgreSQL (local) o acceso a GCP Cloud SQL
Git
```

### 1. Clonar el repositorio

```bash
git clone https://github.com/Closure03/Autolavado.git
cd Autolavado
```

### 2. Configurar el entorno virtual

```bash
cd backend
python -m venv antenv
source antenv/bin/activate        # Windows: antenv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Crea o edita el archivo `backend/.env`:

```env
DATABASE_URL=postgresql://autolavado_user:TU_PASSWORD@IP_GCP:5432/autolavado_db
```

### 4. Inicializar la base de datos

```bash
# Crear la base de datos (si es local):
psql -U postgres -c "CREATE DATABASE autolavado_db;"

# Ejecutar schema y seed:
psql -U postgres -d autolavado_db -f database/schema.sql
psql -U postgres -d autolavado_db -f database/seed.sql
```

### 5. Correr el backend

```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

API disponible en: http://localhost:8000  
Swagger UI en: http://localhost:8000/docs

### 6. Correr el frontend

```bash
cd backend/frontend
python -m http.server 3000
```

Abre: http://localhost:3000

> ⚠️ Recuerda cambiar `API_BASE` en `frontend/script.js` a `http://localhost:8000` para desarrollo local.

---

## ⚙️ Configuración de despliegue en Azure

### Variables de aplicación requeridas en App Service

| Variable | Valor |
|---|---|
| `DATABASE_URL` | `postgresql://autolavado_user:PASSWORD@IP_GCP:5432/autolavado_db` |
| `SCM_DO_BUILD_DURING_DEPLOYMENT` | `true` |

### Comando de inicio (Stack settings)

```
cd backend && pip install -r requirements.txt && uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### CORS en Azure App Service

> ⚠️ La sección **API → CORS** del portal de Azure debe estar **vacía**.
> Si tiene algún valor, Azure sobreescribe el CORS de FastAPI y bloquea las peticiones del frontend.

---

## 🔄 Flujo de despliegue automático

Cada `git push` a la rama `master` dispara automáticamente:

1. **GitHub Actions** compila y valida el código
2. **Azure App Service** recibe el nuevo backend y lo reinicia
3. **Azure Static Web Apps** actualiza el frontend en segundos

---

## 🛠️ Solución de problemas conocidos

| Problema | Causa | Solución |
|---|---|---|
| `Site Disabled (403)` en deploy | App Service detenido | Portal Azure → App Service → Iniciar |
| `cd: can't cd to /home/site/wwwroot/backend` | Ruta absoluta en startup command | Usar ruta relativa: `cd backend && ...` |
| `Failed to fetch` en el frontend | CORS bloqueado por Azure | Vaciar lista en App Service → API → CORS |
| `Application Error` en el navegador | Backend caído o mal startup command | Revisar Log Stream en Kudu |
| `App Directory Location invalid` en Static Web Apps | `app_location` mal configurado | Usar `backend/frontend` sin `./` ni `\` |
| Token inválido en Static Web Apps deploy | Token de Azure vencido | Regenerar en Azure → Administrar token → actualizar secret en GitHub |

---

## 📊 Costos de infraestructura

| Servicio | Plan | Costo estimado |
|---|---|---|
| Azure App Service | B1 Basic | ~$13 USD/mes (cubierto con créditos) |
| Azure Static Web Apps | Free | $0 |
| GCP Cloud SQL | db-f1-micro shared | ~$7 USD/mes (cubierto con créditos) |
| **Total real** | | **$0** (créditos gratuitos) |

---

## 📸 Capturas de pantalla

Ver carpeta `/backend/docs/screenshots/`

---

## 📹 Video de sustentación

Ver archivo `/video/sustentacion.mp4`