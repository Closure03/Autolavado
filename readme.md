# 👥 Equipo de Desarrollo

| Rol                          | Nombre             | GitHub               |
|------------------------------|--------------------|----------------------|
| 🎯 Product Owner / DevOps Lead | **Santiago Garzón** | [@SantiagoGarzon](https://github.com/SantiagoGarzon) |
| ⚙️ Frontend Developer / QA     | **Jonathan Pedroza** | [@JonathanPedroza](https://github.com/JonathanPedroza) |
| 🎨 Backend Developer           | **Mateo Bermejo**   | [@MateoBermejo](https://github.com/MateoBermejo) |

---

# 🚗 Autolavado Cloud Monitoring System

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-orange)
![Grafana](https://img.shields.io/badge/Grafana-Dashboard-F46800)
![Status](https://img.shields.io/badge/Status-Completed-success)

---

## 📖 Descripción

**Autolavado** es una aplicación web para la gestión de vehículos y servicios de lavado, desplegada en contenedores Docker y con monitoreo en tiempo real mediante Prometheus y Grafana.  
Proyecto académico de **Computación en la Nube**, integrando buenas prácticas de despliegue, observabilidad y seguridad.

---

## 🎯 Objetivos

- 🚘 Gestionar vehículos y servicios de autolavado.  
- ⚡ Implementar una API REST moderna con FastAPI.  
- 🗄️ Utilizar PostgreSQL como base de datos.  
- 🐳 Desplegar la solución con Docker Compose.  
- 📈 Implementar observabilidad con Prometheus y Grafana.  
- 🔐 Aplicar seguridad básica mediante API Key.  
- 🔎 Desarrollar búsqueda de vehículos por placa.  

---

## 🏗️ Arquitectura de la Solución

```text
┌──────────────────────┐
│      Frontend        │
│ HTML + CSS + JS      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│     FastAPI API      │
│     Backend REST     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      PostgreSQL      │
│      Database        │
└──────────────────────┘

           │
           ▼

┌──────────────────────┐
│     Prometheus       │
│   Metrics Collector  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      Grafana         │
│      Dashboard       │
└──────────────────────┘
🛠️ Tecnologías Utilizadas
Categoría	Tecnología
Backend	FastAPI
Lenguaje	Python 3.11
ORM	SQLAlchemy
Base de Datos	PostgreSQL 16
Frontend	HTML, CSS, JavaScript
Contenedores	Docker
Orquestación	Docker Compose
Monitoreo	Prometheus
Visualización	Grafana


🚘 Funcionalidades Implementadas
Gestión de Vehículos: Crear, consultar, actualizar, eliminar.

Gestión de Servicios: Registrar, consultar, eliminar.

Relación Vehículo-Servicio: Consultar servicios asociados.

Búsqueda por Placa: Endpoint /api/vehiculos/search?placa=ABC.

🔐 Seguridad
Autenticación mediante API Key.

Operaciones protegidas: POST, PUT, DELETE.

Header requerido:

http
x-api-key: autolavado2026
📈 Observabilidad
Endpoint de métricas: /metrics.

Métricas:

http_requests_total → Total de peticiones.

http_request_duration_seconds → Tiempo de respuesta.

active_vehicles → Vehículos activos.

📊 Dashboard Grafana
Total de solicitudes → http_requests_total

Vehículos activos → active_vehicles

Solicitudes por minuto → rate(http_requests_total[1m])

Latencia promedio →

promql
rate(http_request_duration_seconds_sum[1m]) /
rate(http_request_duration_seconds_count[1m])
📂 Estructura del Proyecto
text
AUTOLAVADO
│
├── backend
│   ├── src
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── frontend
│   │   ├── index.html
│   │   ├── script.js
│   │   └── style.css
│   ├── Dockerfile
│   └── requirements.txt
│
├── prometheus
│   └── prometheus.yml
│
├── docs
│   ├── api-documentation.md
│   ├── security.md
│   └── sprint-retrospectives.md
│
├── traffic.py
├── docker-compose.yml
└── README.md
⚙️ Instalación
bash
git clone <repositorio>
cd Autolavado
docker compose build
docker compose up
🌐 Servicios Disponibles
Servicio	URL
Backend	http://localhost:8000
Swagger	http://localhost:8000/docs
Prometheus	http://localhost:9090
Grafana	http://localhost:3000
Frontend	http://127.0.0.1:5500/backend/frontend/index.html


🚦 Generación de Tráfico
bash
python traffic.py
Genera solicitudes a GET /api/vehiculos para visualizar actividad en Prometheus y Grafana.

🧪 Casos de Prueba
POST /api/vehiculos → Crear vehículo

GET /api/vehiculos → Consultar vehículos

GET /api/vehiculos/search?placa=ABC → Buscar vehículo

PUT /api/vehiculos/{id} → Actualizar vehículo

DELETE /api/vehiculos/{id} → Eliminar vehículo

✅ Estado del Proyecto
Componente	Estado
FastAPI	✅
PostgreSQL	✅
Docker Compose	✅
API Key	✅
Funcionalidad de Búsqueda	✅
Prometheus	✅
Grafana	✅
Frontend	✅
Traffic Generator	✅
Observabilidad	✅


🎉 Resultado Final
Sistema completamente funcional, desplegado en contenedores Docker, con monitoreo en tiempo real, autenticación básica y métricas operacionales listas para observación mediante Prometheus y Grafana.