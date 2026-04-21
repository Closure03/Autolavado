# 🚀 Guía de Despliegue — Google Cloud Platform (Migración desde Azure)

> Arquitectura objetivo:
> **Cloud Run** (backend) + **Cloud Storage** (frontend) + **Cloud SQL** (PostgreSQL)

---

## Prerrequisitos

```bash
# Instalar Google Cloud CLI
# https://cloud.google.com/sdk/docs/install

gcloud auth login
gcloud config set project TU_PROJECT_ID

# Habilitar APIs necesarias
gcloud services enable \
  run.googleapis.com \
  sqladmin.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  storage.googleapis.com
```

---

## FASE 1 — Cloud SQL (PostgreSQL 15)

Si ya tienes la instancia de Cloud SQL del proyecto anterior, sáltate al paso 1.3.

### 1.1 Crear instancia (si no existe)

```bash
gcloud sql instances create autolavado-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --storage-type=SSD \
  --storage-size=10GB \
  --root-password=TU_PASSWORD_ROOT
```

### 1.2 Crear base de datos y usuario

```bash
gcloud sql databases create autolavado_db --instance=autolavado-db
gcloud sql users create autolavado_user \
  --instance=autolavado-db \
  --password=TU_PASSWORD_USER
```

### 1.3 Ejecutar schema y seed

```bash
# Con Cloud SQL Auth Proxy (recomendado)
./cloud-sql-proxy --port 5432 TU_PROJECT_ID:us-central1:autolavado-db &

psql -h 127.0.0.1 -U autolavado_user -d autolavado_db \
  -f backend/database/schema.sql

psql -h 127.0.0.1 -U autolavado_user -d autolavado_db \
  -f backend/database/seed.sql

# Verificar:
psql -h 127.0.0.1 -U autolavado_user -d autolavado_db \
  -c "SELECT COUNT(*) FROM vehiculos;"   # debe ser 10
```

### 1.4 Connection string para Cloud Run

```
# Formato Cloud SQL Auth Proxy (usar en DATABASE_URL):
postgresql://autolavado_user:PASSWORD@/autolavado_db?host=/cloudsql/PROJECT_ID:us-central1:autolavado-db

# Formato IP pública (solo para desarrollo local con IP autorizada):
postgresql://autolavado_user:PASSWORD@IP_PUBLICA:5432/autolavado_db
```

---

## FASE 2 — Artifact Registry

```bash
# Crear repositorio de Docker
gcloud artifacts repositories create autolavado \
  --repository-format=docker \
  --location=us-central1 \
  --description="AutoLavado Cloud — Docker images"

# Configurar Docker para el registry
gcloud auth configure-docker us-central1-docker.pkg.dev
```

---

## FASE 3 — Build y Deploy del Backend en Cloud Run

### 3.1 Construir y subir la imagen Docker

```bash
cd backend

# Build
docker build -t us-central1-docker.pkg.dev/PROJECT_ID/autolavado/autolavado-api:latest .

# Push
docker push us-central1-docker.pkg.dev/PROJECT_ID/autolavado/autolavado-api:latest
```

### 3.2 Deploy en Cloud Run

```bash
gcloud run deploy autolavado-api \
  --image us-central1-docker.pkg.dev/PROJECT_ID/autolavado/autolavado-api:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "DATABASE_URL=postgresql://autolavado_user:PASSWORD@/autolavado_db?host=/cloudsql/PROJECT_ID:us-central1:autolavado-db" \
  --add-cloudsql-instances PROJECT_ID:us-central1:autolavado-db \
  --memory 512Mi \
  --cpu 1 \
  --port 8080 \
  --min-instances 0 \
  --max-instances 3
```

### 3.3 Obtener la URL del servicio

```bash
gcloud run services describe autolavado-api \
  --region us-central1 \
  --format 'value(status.url)'
# Ejemplo: https://autolavado-api-abc123-uc.a.run.app
```

### 3.4 Verificar el backend

```bash
# Health check
curl https://autolavado-api-XXXX-uc.a.run.app/

# Listar vehículos
curl https://autolavado-api-XXXX-uc.a.run.app/api/vehiculos

# Swagger UI — abrir en navegador:
# https://autolavado-api-XXXX-uc.a.run.app/docs
```

---

## FASE 4 — Deploy del Frontend en Cloud Storage

### 4.1 Actualizar API_BASE en script.js

```javascript
// backend/frontend/script.js — línea 7
// Reemplazar con la URL real de Cloud Run:
const API_BASE = "https://autolavado-api-XXXX-uc.a.run.app";
```

### 4.2 Crear el bucket

```bash
# Crear bucket con nombre único (el nombre debe ser globalmente único en GCP)
gsutil mb -p PROJECT_ID -l us-central1 gs://autolavado-frontend

# Habilitar acceso público
gsutil iam ch allUsers:objectViewer gs://autolavado-frontend

# Configurar como sitio web estático
gsutil web set -m index.html -e 404.html gs://autolavado-frontend
```

### 4.3 Subir los archivos

```bash
gsutil -m cp -r backend/frontend/* gs://autolavado-frontend/
```

### 4.4 URL del frontend

```
https://storage.googleapis.com/autolavado-frontend/index.html
```

---

## FASE 5 — Configurar Secrets en GitHub

Ve a: `github.com/Closure03/Autolavado → Settings → Secrets and variables → Actions`

Agrega los siguientes secrets:

| Secret | Valor |
|---|---|
| `GCP_PROJECT_ID` | Tu Project ID de GCP (ej: `mi-proyecto-123456`) |
| `GCP_SA_KEY` | JSON de la Service Account con permisos de Cloud Run, Artifact Registry y Storage |
| `DATABASE_URL` | Connection string completo de Cloud SQL |

### Crear Service Account para GitHub Actions

```bash
# Crear service account
gcloud iam service-accounts create github-actions-sa \
  --display-name="GitHub Actions — AutoLavado"

# Asignar roles necesarios
for ROLE in \
  roles/run.admin \
  roles/artifactregistry.writer \
  roles/storage.admin \
  roles/cloudsql.client \
  roles/iam.serviceAccountUser; do
  gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:github-actions-sa@PROJECT_ID.iam.gserviceaccount.com" \
    --role="$ROLE"
done

# Generar key JSON (copiar el contenido al secret GCP_SA_KEY)
gcloud iam service-accounts keys create gcp-key.json \
  --iam-account=github-actions-sa@PROJECT_ID.iam.gserviceaccount.com

cat gcp-key.json   # Copiar todo el contenido al secret
rm gcp-key.json    # Eliminar el archivo local
```

---

## Diferencias clave: Azure → GCP

| Aspecto | Azure (anterior) | GCP (actual) |
|---|---|---|
| Backend hosting | App Service (B1) | Cloud Run (serverless) |
| Frontend hosting | Static Web Apps | Cloud Storage (bucket público) |
| Startup command | `cd backend && uvicorn...` | Variable `PORT` en Dockerfile |
| CORS | Vaciar lista en portal | `allow_origins` en FastAPI |
| DB connection | IP pública + SSL | Cloud SQL Auth Proxy |
| Costo estimado | ~$13/mes | ~$7/mes (Cloud Run cobra por uso) |

---

## Solución de problemas

| Problema | Solución |
|---|---|
| `PORT variable not set` en Cloud Run | El `CMD` del Dockerfile debe usar `${PORT:-8080}` |
| `Error 503` en Cloud Run | Verificar que `--allow-unauthenticated` está configurado |
| CORS bloqueado | Verificar `API_BASE` en `script.js` apunta a la URL de Cloud Run |
| `Cloud SQL connection refused` | Agregar `--add-cloudsql-instances` en el deploy de Cloud Run |
| Bucket 403 | Ejecutar `gsutil iam ch allUsers:objectViewer gs://BUCKET` |
