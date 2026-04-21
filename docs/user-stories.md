# 📖 Historias de Usuario — AutoLavado Cloud

> Mínimo 6 historias por integrante (2 por sprint)
> Total: 18 historias — 3 sprints × 3 integrantes × 2 historias

---

## 🔵 SPRINT 1 — Backend y Base de Datos

---

### HU-01 — Modelo de datos: Vehículo
**Responsable:** @MateoBermejo | **Sprint:** 1 | **Prioridad:** Alta | **Estimación:** 3 pts | **Tipo:** Feature

```
Como desarrollador backend
Quiero definir el modelo de datos para Vehículo con SQLAlchemy
Para persistir correctamente la información de los vehículos en PostgreSQL
```

**Criterios de Aceptación:**
- [ ] Modelo `Vehiculo` creado en `models.py` con campos: id, placa, marca, modelo, anio, color, tipo, propietario, telefono, created_at
- [ ] Campo `placa` es único en la base de datos
- [ ] Relación 1→N con `Servicio` configurada con `cascade="all, delete"`
- [ ] Schema Pydantic `VehiculoCreate` y `VehiculoOut` creados en `schemas.py`
- [ ] Validación de placa en mayúsculas con `field_validator`

---

### HU-02 — Modelo de datos: Servicio
**Responsable:** @MateoBermejo | **Sprint:** 1 | **Prioridad:** Alta | **Estimación:** 3 pts | **Tipo:** Feature

```
Como desarrollador backend
Quiero definir el modelo de datos para Servicio con SQLAlchemy
Para registrar el historial de lavados asociados a cada vehículo
```

**Criterios de Aceptación:**
- [ ] Modelo `Servicio` creado con campos: id, vehiculo_id, tipo_servicio, precio, estado, observaciones, fecha_servicio, created_at
- [ ] FK `vehiculo_id` referencia a `vehiculos.id` con `ON DELETE CASCADE`
- [ ] Enum de tipos: lavado_basico, lavado_completo, lavado_premium, encerado, tapizado, motor
- [ ] Enum de estados: pendiente, en_proceso, completado, cancelado
- [ ] Schema `ServicioCreate` y `ServicioOut` creados y validados

---

### HU-03 — API CRUD de Vehículos
**Responsable:** @MateoBermejo | **Sprint:** 1 | **Prioridad:** Alta | **Estimación:** 5 pts | **Tipo:** Feature

```
Como administrador del autolavado
Quiero un API REST con operaciones CRUD para vehículos
Para gestionar el registro de clientes y sus vehículos desde cualquier interfaz
```

**Criterios de Aceptación:**
- [ ] `GET /api/vehiculos` retorna lista de todos los vehículos (200)
- [ ] `GET /api/vehiculos/{id}` retorna un vehículo o 404
- [ ] `POST /api/vehiculos` crea vehículo, retorna 201, valida placa duplicada
- [ ] `PUT /api/vehiculos/{id}` actualiza vehículo, retorna 200 o 404
- [ ] `DELETE /api/vehiculos/{id}` elimina vehículo y sus servicios (CASCADE), retorna 204
- [ ] Todos los endpoints documentados en Swagger (`/docs`)

---

### HU-04 — API CRUD de Servicios y relación
**Responsable:** @MateoBermejo | **Sprint:** 1 | **Prioridad:** Alta | **Estimación:** 5 pts | **Tipo:** Feature

```
Como operario del autolavado
Quiero registrar, listar y eliminar servicios desde la API
Para llevar un historial completo de los trabajos realizados a cada vehículo
```

**Criterios de Aceptación:**
- [ ] `GET /api/servicios` retorna todos los servicios (200)
- [ ] `POST /api/servicios` crea servicio, valida que `vehiculo_id` exista
- [ ] `DELETE /api/servicios/{id}` elimina servicio, retorna 204 o 404
- [ ] `GET /api/vehiculos/{id}/servicios` retorna historial ordenado por fecha desc
- [ ] Manejo correcto de errores con `HTTPException` y códigos HTTP estándar

---

### HU-05 — Configurar Cloud SQL en GCP
**Responsable:** @SantiagoGarzon | **Sprint:** 1 | **Prioridad:** Alta | **Estimación:** 3 pts | **Tipo:** DevOps

```
Como DevOps del equipo
Quiero crear y configurar la instancia de Cloud SQL en GCP
Para que el backend tenga una base de datos PostgreSQL disponible en producción
```

**Criterios de Aceptación:**
- [ ] Instancia `autolavado-db` creada en GCP Cloud SQL (PostgreSQL 15, us-central1)
- [ ] Base de datos `autolavado_db` y usuario `autolavado_user` creados
- [ ] `schema.sql` y `seed.sql` ejecutados correctamente (10 vehículos, 12 servicios)
- [ ] Connection string documentada en formato Cloud SQL Auth Proxy
- [ ] Secret `DATABASE_URL` configurado en GitHub Actions

---

### HU-06 — Dockerfile y pipeline CI/CD inicial
**Responsable:** @SantiagoGarzon | **Sprint:** 1 | **Prioridad:** Alta | **Estimación:** 5 pts | **Tipo:** DevOps

```
Como DevOps del equipo
Quiero containerizar el backend con Docker y configurar el pipeline de CI/CD
Para automatizar el build y despliegue en cada push a main
```

**Criterios de Aceptación:**
- [ ] `Dockerfile` creado en `backend/` con Python 3.11-slim
- [ ] `.dockerignore` configurado correctamente
- [ ] Imagen buildea sin errores: `docker build -t autolavado-api .`
- [ ] Workflow `gcp-backend-deploy.yml` creado en `.github/workflows/`
- [ ] El pipeline se ejecuta automáticamente en push a `main`
- [ ] Secrets de GCP (`GCP_SA_KEY`, `GCP_PROJECT_ID`) configurados en GitHub

---

## 🟢 SPRINT 2 — Frontend e Integración Cloud

---

### HU-07 — Vista de listado de vehículos
**Responsable:** @JhonatanPedroza | **Sprint:** 2 | **Prioridad:** Alta | **Estimación:** 3 pts | **Tipo:** Feature

```
Como usuario del sistema
Quiero ver todos los vehículos registrados en una tabla
Para consultar rápidamente los clientes y sus datos
```

**Criterios de Aceptación:**
- [ ] Tabla con columnas: ID, Placa, Marca/Modelo, Tipo, Propietario, Teléfono, Acciones
- [ ] La tabla carga los datos desde `GET /api/vehiculos`
- [ ] Indicador de carga mientras se obtienen los datos
- [ ] Mensaje de error si la API no responde
- [ ] Botones de acción: Ver historial, Editar, Eliminar
- [ ] Diseño responsive con paleta de colores Azure/GCP

---

### HU-08 — Formulario crear y editar vehículo
**Responsable:** @JhonatanPedroza | **Sprint:** 2 | **Prioridad:** Alta | **Estimación:** 5 pts | **Tipo:** Feature

```
Como operario del autolavado
Quiero un formulario para registrar y actualizar vehículos
Para ingresar nuevos clientes y corregir información existente
```

**Criterios de Aceptación:**
- [ ] Formulario con campos: Placa, Marca, Modelo, Año, Color, Tipo, Propietario, Teléfono
- [ ] `POST /api/vehiculos` al crear (status 201 = éxito)
- [ ] `PUT /api/vehiculos/{id}` al editar (precarga datos del vehículo)
- [ ] Validación de campos obligatorios en el cliente (Placa, Marca, Modelo, Propietario)
- [ ] Toast de confirmación al guardar exitosamente
- [ ] Toast de error con el mensaje del servidor si falla

---

### HU-09 — Modal historial de servicios por vehículo
**Responsable:** @JhonatanPedroza | **Sprint:** 2 | **Prioridad:** Media | **Estimación:** 3 pts | **Tipo:** Feature

```
Como administrador
Quiero ver el historial de servicios de un vehículo en un modal
Para consultar el registro completo de lavados sin salir de la vista principal
```

**Criterios de Aceptación:**
- [ ] Modal se abre al hacer clic en "Ver historial"
- [ ] Consume `GET /api/vehiculos/{id}/servicios`
- [ ] Muestra: tipo de servicio, precio formateado en COP, estado con badge de color, fecha
- [ ] Muestra total acumulado de servicios completados
- [ ] Mensaje "Sin servicios registrados" si el vehículo no tiene historial
- [ ] Modal se cierra con X o clic fuera del contenedor

---

### HU-10 — CORS y variables de entorno en producción
**Responsable:** @MateoBermejo | **Sprint:** 2 | **Prioridad:** Alta | **Estimación:** 2 pts | **Tipo:** DevOps

```
Como desarrollador backend
Quiero configurar CORS correctamente para el entorno de producción en GCP
Para que el frontend en Cloud Storage pueda consumir la API en Cloud Run sin errores
```

**Criterios de Aceptación:**
- [ ] `CORSMiddleware` configurado en `main.py` con `allow_origins=["*"]` para dev
- [ ] Variable de entorno `FRONTEND_URL` usada en producción para restringir origen
- [ ] La sección CORS de GCP Cloud Run no interfiere con el middleware de FastAPI
- [ ] Prueba exitosa desde el navegador sin errores de CORS en la consola
- [ ] `.env.example` documentado con todas las variables necesarias

---

### HU-11 — Deploy backend en Cloud Run
**Responsable:** @SantiagoGarzon | **Sprint:** 2 | **Prioridad:** Alta | **Estimación:** 5 pts | **Tipo:** DevOps

```
Como DevOps
Quiero desplegar el backend FastAPI en Google Cloud Run
Para tener la API accesible públicamente con escalado automático y sin gestión de servidores
```

**Criterios de Aceptación:**
- [ ] Imagen Docker publicada en Artifact Registry: `us-central1-docker.pkg.dev/PROJECT/autolavado/api`
- [ ] Servicio Cloud Run `autolavado-api` creado en us-central1
- [ ] Variable `DATABASE_URL` configurada con conexión a Cloud SQL via Auth Proxy
- [ ] Servicio accesible públicamente: `GET /` retorna `{"status":"ok"}`
- [ ] `GET /api/vehiculos` retorna los 10 vehículos del seed
- [ ] URL del servicio documentada en el README

---

### HU-12 — Deploy frontend en Cloud Storage
**Responsable:** @SantiagoGarzon | **Sprint:** 2 | **Prioridad:** Alta | **Estimación:** 3 pts | **Tipo:** DevOps

```
Como DevOps
Quiero desplegar el frontend estático en Google Cloud Storage con acceso público
Para que los usuarios accedan a la interfaz sin necesidad de un servidor web
```

**Criterios de Aceptación:**
- [ ] Bucket `autolavado-frontend` creado en GCP con acceso público
- [ ] Archivos `index.html`, `style.css`, `script.js` subidos al bucket
- [ ] `script.js` tiene `API_BASE` apuntando a la URL de Cloud Run en producción
- [ ] Sitio web estático habilitado en el bucket con `index.html` como página principal
- [ ] URL pública funciona y carga el frontend correctamente
- [ ] Workflow `gcp-frontend-deploy.yml` automatiza el deploy en cada push

---

## 🟡 SPRINT 3 — Estabilización, Pruebas y Documentación

---

### HU-13 — Pruebas de integración E2E
**Responsable:** @MateoBermejo | **Sprint:** 3 | **Prioridad:** Alta | **Estimación:** 5 pts | **Tipo:** QA

```
Como QA del equipo
Quiero ejecutar pruebas de integración que verifiquen el flujo completo
Para garantizar que frontend, backend y base de datos funcionan correctamente juntos
```

**Criterios de Aceptación:**
- [ ] Prueba: crear vehículo → verificar en DB → eliminar
- [ ] Prueba: registrar servicio → verificar en historial → eliminar
- [ ] Prueba: CORS verificado desde el dominio del frontend en GCP
- [ ] Todos los endpoints retornan los status HTTP correctos
- [ ] Resultados de pruebas documentados en `docs/sprint-retrospectives.md`
- [ ] Bugs encontrados registrados como Issues en GitHub con label `bug`

---

### HU-14 — Documentación de API con Swagger
**Responsable:** @JhonatanPedroza | **Sprint:** 3 | **Prioridad:** Media | **Estimación:** 3 pts | **Tipo:** Documentation

```
Como desarrollador externo
Quiero acceder a la documentación completa de la API
Para poder integrar el sistema con otras aplicaciones sin ambigüedades
```

**Criterios de Aceptación:**
- [ ] `api-documentation.md` con todos los endpoints documentados
- [ ] Cada endpoint incluye: método, ruta, parámetros, body ejemplo, response ejemplo
- [ ] Códigos de error documentados con su significado
- [ ] Swagger UI accesible en `/docs` de la URL de Cloud Run
- [ ] Ejemplos de `curl` funcionales para cada endpoint

---

### HU-15 — Guía de despliegue GCP
**Responsable:** @JhonatanPedroza | **Sprint:** 3 | **Prioridad:** Media | **Estimación:** 3 pts | **Tipo:** Documentation

```
Como nuevo miembro del equipo
Quiero una guía paso a paso para desplegar el sistema en GCP
Para poder replicar el entorno de producción desde cero
```

**Criterios de Aceptación:**
- [ ] `deployment-guide-gcp.md` con los 3 pasos: Cloud SQL → Cloud Run → Cloud Storage
- [ ] Comandos `gcloud` exactos para cada paso
- [ ] Sección de solución de problemas comunes
- [ ] Variables de entorno documentadas con sus valores de ejemplo
- [ ] Diagrama de arquitectura incluido

---

### HU-16 — Monitoreo con Cloud Logging
**Responsable:** @SantiagoGarzon | **Sprint:** 3 | **Prioridad:** Baja | **Estimación:** 3 pts | **Tipo:** DevOps

```
Como DevOps
Quiero configurar Cloud Logging para el servicio de Cloud Run
Para monitorear errores y el comportamiento de la API en producción
```

**Criterios de Aceptación:**
- [ ] Logs de la aplicación visibles en GCP Cloud Logging
- [ ] Filtro configurado para ver solo logs de `autolavado-api`
- [ ] Alerta configurada para errores 500 en la API
- [ ] Captura de pantalla del dashboard de logs incluida en `docs/screenshots/`
- [ ] Instrucciones para acceder a logs documentadas en el README

---

### HU-17 — README completo del proyecto
**Responsable:** @SantiagoGarzon | **Sprint:** 3 | **Prioridad:** Alta | **Estimación:** 2 pts | **Tipo:** Documentation

```
Como evaluador del proyecto
Quiero leer un README completo y profesional
Para entender el proyecto, el equipo, la arquitectura y cómo ejecutarlo
```

**Criterios de Aceptación:**
- [ ] README incluye: descripción, equipo con roles, arquitectura, sprint completados
- [ ] Diagrama de arquitectura GCP incluido
- [ ] Instrucciones de instalación local paso a paso
- [ ] URLs de producción actualizadas y funcionando
- [ ] Métricas del proyecto (velocity, historias completadas, bugs)
- [ ] Sección de lecciones aprendidas con al menos 5 items

---

### HU-18 — Retrospectiva y métricas de sprints
**Responsable:** @MateoBermejo | **Sprint:** 3 | **Prioridad:** Media | **Estimación:** 2 pts | **Tipo:** Documentation

```
Como Product Owner
Quiero documentar las métricas y lecciones aprendidas de cada sprint
Para demostrar el proceso ágil y las mejoras continuas del equipo
```

**Criterios de Aceptación:**
- [ ] `sprint-retrospectives.md` con sección por cada sprint
- [ ] Cada sprint documenta: qué salió bien, qué mejorar, velocity, bugs
- [ ] Burndown chart descrito (aunque sea en texto/tabla)
- [ ] Throughput: historias completadas por sprint documentadas
- [ ] Lead time y cycle time estimados para al menos 3 historias
- [ ] Evidencia de participación equitativa de los 3 integrantes

---

## 📊 Resumen de distribución

| Sprint | @SantiagoGarzon | @MateoBermejo | @JhonatanPedroza | Total pts |
|---|---|---|---|---|
| Sprint 1 | HU-05 (3), HU-06 (5) | HU-01 (3), HU-02 (3), HU-03 (5), HU-04 (5) | — | 24 |
| Sprint 2 | HU-11 (5), HU-12 (3) | HU-10 (2) | HU-07 (3), HU-08 (5), HU-09 (3) | 21 |
| Sprint 3 | HU-16 (3), HU-17 (2) | HU-13 (5), HU-18 (2) | HU-14 (3), HU-15 (3) | 18 |
| **Total** | **18 pts** | **25 pts** | **17 pts** | **63 pts** |

> **Nota:** Mateo lidera el backend (Sprint 1 intensivo). El balance se iguala en Sprints 2 y 3 donde Jhonatan y Santiago asumen más carga.
