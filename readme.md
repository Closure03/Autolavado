# 🚗 AutoLavado Cloud — Gestión Colaborativa con GitHub Projects

> **Proyecto 2 — Desarrollo de Aplicaciones en la Nube**
> Fundación Universitaria Los Libertadores

[![Deploy Backend](https://github.com/Closure03/Autolavado/actions/workflows/gcp-backend-deploy.yml/badge.svg)](https://github.com/Closure03/Autolavado/actions)
[![Deploy Frontend](https://github.com/Closure03/Autolavado/actions/workflows/gcp-frontend-deploy.yml/badge.svg)](https://github.com/Closure03/Autolavado/actions)

---

## 👥 Equipo de Desarrollo

| Rol | Nombre | GitHub |
|---|---|---|
| 🎯 Product Owner / DevOps Lead | **Santiago Garzón** | @SantiagoGarzon |
| ⚙️ Frontend Developer / QA | **Mateo Bermejo** | @MateoBermejo |
| 🎨 Backend Developer | **Jonathan Pedroza** | @JonathanPedroza |

---

## 📋 Descripción del Proyecto

Sistema CRUD full-stack para la gestión de vehículos y servicios de un autolavado. Desarrollado colaborativamente en 3 sprints con metodología **Kanban**, integrando CI/CD automático y despliegue completo en **Google Cloud Platform**.

---

## 🏗️ Arquitectura

| Componente | Tecnología | Servicio GCP |
|---|---|---|
| **Frontend** | HTML5 / CSS3 / JavaScript | Cloud Storage + Cloud CDN |
| **Backend** | FastAPI (Python 3.11) | Cloud Run |
| **Base de datos** | PostgreSQL 15 | Cloud SQL |
| **CI/CD** | GitHub Actions | Cloud Build (opcional) |
| **Contenedores** | Docker | Artifact Registry |
| **Infraestructura** | GCP | us-central1 |

### Diagrama de arquitectura

```
┌──────────────────────────────────────────────────────┐
│               GOOGLE CLOUD PLATFORM                  │
│                                                      │
│  ┌──────────────────────┐                            │
│  │  Cloud Storage       │  Frontend HTML/CSS/JS      │
│  │  + Cloud CDN         │  autolavado-frontend       │
│  └──────────┬───────────┘                            │
│             │ HTTPS                                  │
│             ▼                                        │
│  ┌──────────────────────┐                            │
│  │  Cloud Run           │  Backend FastAPI           │
│  │  (Docker Container)  │  autolavado-api            │
│  └──────────┬───────────┘                            │
│             │ TCP 5432                               │
│             ▼                                        │
│  ┌──────────────────────┐                            │
│  │  Cloud SQL           │  PostgreSQL 15             │
│  │  autolavado-db       │  us-central1               │
│  └──────────────────────┘                            │
└──────────────────────────────────────────────────────┘
```

---

## 📊 GitHub Project — Tablero Kanban

🔗 **[Ver GitHub Project](https://github.com/Closure03/Autolavado/projects)**

### Columnas del tablero

| Columna | Descripción |
|---|---|
| **Backlog** | Historias pendientes de priorizar |
| **Ready** | Listas para iniciar en el sprint |
| **In Progress** | En desarrollo activo |
| **Review** | En code review / PR abierto |
| **Done** | Completadas y mergeadas |

### Campos personalizados configurados

| Campo | Opciones |
|---|---|
| Sprint | Sprint 1, Sprint 2, Sprint 3 |
| Responsable | @SantiagoGarzon, @MateoBermejo, @JhonatanPedroza |
| Prioridad | Alta, Media, Baja |
| Estimación | 1, 2, 3, 5, 8 (puntos de historia) |
| Tipo | Feature, Bug, Documentation, DevOps |

---

## 🗂️ Estructura del Repositorio

```
Autolavado/
├── .github/
│   ├── workflows/
│   │   ├── project-automation.yml      # Mueve cards automáticamente
│   │   ├── gcp-backend-deploy.yml      # Deploy backend → Cloud Run
│   │   └── gcp-frontend-deploy.yml     # Deploy frontend → Cloud Storage
│   └── PULL_REQUEST_TEMPLATE.md
├── backend/
│   ├── database/
│   │   ├── schema.sql
│   │   └── seed.sql
│   ├── docs/
│   ├── frontend/
│   │   ├── index.html
│   │   ├── style.css
│   │   └── script.js
│   ├── src/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── database.py
│   ├── Dockerfile                      # Contenedor del backend
│   ├── .dockerignore
│   └── requirements.txt
├── docs/
│   ├── user-stories.md                 # Todas las historias de usuario
│   ├── api-documentation.md
│   ├── deployment-guide-gcp.md
│   ├── sprint-retrospectives.md
│   └── screenshots/
├── video/
│   └── sustentacion.mp4
└── readme.md
```

---

## 🏃 Estrategia de Ramas

```
main (producción — protegida)
└── development (integración)
    ├── feature/sprint1-backend-models          → @MateoBermejo
    ├── feature/sprint1-database-setup          → @MateoBermejo
    ├── feature/sprint1-api-vehiculos           → @MateoBermejo
    ├── feature/sprint1-api-servicios           → @MateoBermejo
    ├── feature/sprint1-ci-cd-pipeline          → @SantiagoGarzon
    ├── feature/sprint1-docker-config           → @SantiagoGarzon
    ├── feature/sprint2-frontend-vehiculos      → @JhonatanPedroza
    ├── feature/sprint2-frontend-servicios      → @JhonatanPedroza
    ├── feature/sprint2-frontend-historial      → @JhonatanPedroza
    ├── feature/sprint2-cors-config             → @MateoBermejo
    ├── feature/sprint2-gcp-cloud-run           → @SantiagoGarzon
    ├── feature/sprint2-gcp-cloud-storage       → @SantiagoGarzon
    ├── feature/sprint3-deploy-backend          → @SantiagoGarzon
    ├── feature/sprint3-deploy-frontend         → @JhonatanPedroza
    ├── feature/sprint3-monitoring              → @SantiagoGarzon
    ├── feature/sprint3-documentation           → @JhonatanPedroza
    ├── feature/sprint3-readme                  → @SantiagoGarzon
    └── feature/sprint3-final-testing           → @MateoBermejo
```

### Flujo de trabajo

1. Crear rama `feature/sprintN-funcionalidad` desde `development`
2. Desarrollar la funcionalidad
3. Abrir Pull Request con descripción y criterios de aceptación
4. Code review obligatorio de al menos 1 compañero
5. Merge a `development` tras aprobación
6. Testing en `development`
7. Release: merge `development` → `main`

---

## 🚀 Sprints Completados

### Sprint 1 — Backend y Base de Datos

**Objetivo:** Tener la API REST funcional conectada a Cloud SQL

| Historia | Responsable | Estado | Puntos |
|---|---|---|---|
| HU-01: Modelo de datos Vehículo | @MateoBermejo | ✅ Done | 3 |
| HU-02: Modelo de datos Servicio | @MateoBermejo | ✅ Done | 3 |
| HU-03: Endpoint CRUD Vehículos | @MateoBermejo | ✅ Done | 5 |
| HU-04: Endpoint CRUD Servicios | @MateoBermejo | ✅ Done | 5 |
| HU-05: Configurar Cloud SQL | @SantiagoGarzon | ✅ Done | 3 |
| HU-06: Docker + CI/CD pipeline | @SantiagoGarzon | ✅ Done | 5 |

**Velocity Sprint 1:** 24 puntos

### Sprint 2 — Frontend e Integración

**Objetivo:** Frontend conectado a la API y desplegado en Cloud Storage

| Historia | Responsable | Estado | Puntos |
|---|---|---|---|
| HU-07: Vista listado de vehículos | @JhonatanPedroza | ✅ Done | 3 |
| HU-08: Formulario crear/editar vehículo | @JhonatanPedroza | ✅ Done | 5 |
| HU-09: Vista historial de servicios | @JhonatanPedroza | ✅ Done | 3 |
| HU-10: Configurar CORS en backend | @MateoBermejo | ✅ Done | 2 |
| HU-11: Deploy backend en Cloud Run | @SantiagoGarzon | ✅ Done | 5 |
| HU-12: Deploy frontend en Cloud Storage | @SantiagoGarzon | ✅ Done | 3 |

**Velocity Sprint 2:** 21 puntos

### Sprint 3 — Despliegue, Pruebas y Documentación

**Objetivo:** Sistema estable en producción, documentado y probado

| Historia | Responsable | Estado | Puntos |
|---|---|---|---|
| HU-13: Pruebas de integración E2E | @MateoBermejo | ✅ Done | 5 |
| HU-14: Documentación de API | @JhonatanPedroza | ✅ Done | 3 |
| HU-15: Guía de despliegue GCP | @JhonatanPedroza | ✅ Done | 3 |
| HU-16: Monitoreo Cloud Logging | @SantiagoGarzon | ✅ Done | 3 |
| HU-17: README completo | @SantiagoGarzon | ✅ Done | 2 |
| HU-18: Retrospectiva y métricas | @MateoBermejo | ✅ Done | 2 |

**Velocity Sprint 3:** 18 puntos

---

## 📈 Métricas del Proyecto

| Métrica | Valor |
|---|---|
| **Velocity promedio** | 21 puntos por sprint |
| **Historias completadas** | 18/18 |
| **Total puntos entregados** | 63 puntos |
| **Bugs encontrados** | 6 |
| **Tiempo promedio de resolución** | 4 horas |
| **Pull Requests mergeados** | 18 |
| **Code reviews realizados** | 18 |

---

## 🌐 URLs en Producción (GCP)

| Componente | URL |
|---|---|
| **Frontend** | https://storage.googleapis.com/autolavado-frontend/index.html |
| **Backend API** | https://autolavado-api-XXXX-uc.a.run.app |
| **Swagger UI** | https://autolavado-api-XXXX-uc.a.run.app/docs |
| **GitHub Project** | https://github.com/Closure03/Autolavado/projects |

---

## ⚙️ Instalación y Uso Local

### Prerrequisitos

```
Python 3.11+
Docker
gcloud CLI
Git
```

### 1. Clonar el repositorio

```bash
git clone https://github.com/Closure03/Autolavado.git
cd Autolavado
git checkout development
```

### 2. Configurar variables de entorno

```bash
cp backend/.env.example backend/.env
# Editar backend/.env con tus credenciales de Cloud SQL
```

```env
DATABASE_URL=postgresql://autolavado_user:PASSWORD@/autolavado_db?host=/cloudsql/PROJECT_ID:us-central1:autolavado-db
```

### 3. Correr con Docker localmente

```bash
cd backend
docker build -t autolavado-api .
docker run -p 8000:8000 --env-file .env autolavado-api
```

### 4. Correr sin Docker

```bash
cd backend
python -m venv antenv && source antenv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000
```

### 5. Frontend local

```bash
cd backend/frontend
python -m http.server 3000
# http://localhost:3000
```

---

## 📚 Lecciones Aprendidas

| Desafío | Lección |
|---|---|
| YAML del frontend tenía barra invertida `\` | Los paths en YAML siempre con `/` en cualquier SO |
| Cloud Run requiere `PORT` como variable de entorno | Uvicorn debe escuchar en `$PORT`, no en `8000` hardcodeado |
| CORS bloqueado entre Cloud Storage y Cloud Run | Configurar `allow_origins` con la URL exacta del bucket |
| Secrets de GCP en GitHub Actions | Usar `google-github-actions/auth` con Workload Identity |
| La rama `main` se rompió en un merge | Proteger `main` con branch protection rules desde el inicio |

---

## 🔗 Enlaces Importantes

- [Aplicación en producción](https://storage.googleapis.com/autolavado-frontend/index.html)
- [GitHub Project — Tablero Kanban](https://github.com/Closure03/Autolavado/projects)
- [Historias de usuario](./docs/user-stories.md)
- [Guía de despliegue GCP](./docs/deployment-guide-gcp.md)
- [Documentación de API](./backend/docs/api-documentation.md)
- [Retrospectivas de sprint](./docs/sprint-retrospectives.md)
