# 📊 Retrospectivas y Métricas de Sprints — AutoLavado Cloud

---

## Sprint 1 — Backend y Base de Datos

**Duración:** Semana 1  
**Objetivo:** API REST funcional con Cloud SQL  
**Velocity:** 24 puntos

### ✅ Qué salió bien
- El modelo de datos quedó bien definido desde el inicio, evitando refactors
- La conexión a Cloud SQL funcionó en el primer intento con el Auth Proxy
- Buena comunicación en el equipo para dividir los endpoints sin conflictos

### 🔧 Qué mejorar
- El Dockerfile tuvo que rehacerse porque usaba `PORT 8000` fijo en lugar de `$PORT`
- Los secrets de GitHub Actions tomaron más tiempo del esperado en configurarse
- Faltó escribir pruebas desde el inicio (se dejó para Sprint 3)

### 📈 Métricas

| Métrica | Valor |
|---|---|
| Historias planificadas | 6 |
| Historias completadas | 6 |
| Puntos planificados | 24 |
| Puntos entregados | 24 |
| Bugs encontrados | 2 |
| PRs mergeados | 6 |

### Bugs Sprint 1
- **BUG-01:** `PORT` hardcodeado en Dockerfile — no iniciaba en Cloud Run → fix en Dockerfile
- **BUG-02:** `psycopg2-binary` no instalaba en Alpine Linux → cambiado a `python:3.11-slim`

### Lead Time promedio (backlog → done)
- HU-01: ~6 horas
- HU-05: ~8 horas (configuración GCP tomó más de lo esperado)

---

## Sprint 2 — Frontend e Integración Cloud

**Duración:** Semana 2  
**Objetivo:** Frontend conectado a la API, sistema completo en GCP  
**Velocity:** 21 puntos

### ✅ Qué salió bien
- El frontend se integró perfectamente con la API tras resolver el CORS
- Cloud Storage resultó muy sencillo de configurar comparado con Static Web Apps de Azure
- Code reviews mejoraron la calidad del código (se detectó XSS en el input de placa)

### 🔧 Qué mejorar
- El error de CORS tardó 2 horas en diagnosticarse (faltaba `allow_origins` correcto)
- La rama `feature/sprint2-gcp-cloud-run` tuvo conflictos con `development` al mergear
- Faltó probar en diferentes navegadores antes de marcar como Done

### 📈 Métricas

| Métrica | Valor |
|---|---|
| Historias planificadas | 6 |
| Historias completadas | 6 |
| Puntos planificados | 21 |
| Puntos entregados | 21 |
| Bugs encontrados | 3 |
| PRs mergeados | 6 |

### Bugs Sprint 2
- **BUG-03:** CORS bloqueaba peticiones del bucket al Cloud Run → `allow_origins=["*"]`
- **BUG-04:** `API_BASE` con barra final `/` en script.js rompía algunas rutas → removida
- **BUG-05:** Precio en formulario aceptaba valores negativos → validación `min="0"` en HTML

### Cycle Time promedio (in progress → done)
- HU-07: ~4 horas
- HU-11: ~6 horas
- HU-12: ~2 horas

---

## Sprint 3 — Estabilización, Pruebas y Documentación

**Duración:** Semana 3  
**Objetivo:** Sistema probado, documentado y listo para sustentación  
**Velocity:** 18 puntos

### ✅ Qué salió bien
- Las pruebas E2E encontraron 1 bug crítico antes de la entrega (BUG-06)
- La documentación quedó completa y organizada
- Cloud Logging facilitó mucho el diagnóstico de errores en producción

### 🔧 Qué mejorar
- La documentación debería escribirse durante el desarrollo, no al final
- El monitoreo debería configurarse desde el Sprint 1
- Faltó implementar pruebas automatizadas (pytest) en el pipeline

### 📈 Métricas

| Métrica | Valor |
|---|---|
| Historias planificadas | 6 |
| Historias completadas | 6 |
| Puntos planificados | 18 |
| Puntos entregados | 18 |
| Bugs encontrados | 1 |
| PRs mergeados | 6 |

### Bugs Sprint 3
- **BUG-06:** DELETE `/api/vehiculos/{id}` retornaba 500 cuando el vehículo tenía servicios activos → verificado que CASCADE funciona correctamente en Cloud SQL

---

## 📊 Resumen General del Proyecto

| Sprint | Puntos planificados | Puntos entregados | Bugs | PRs |
|---|---|---|---|---|
| Sprint 1 | 24 | 24 | 2 | 6 |
| Sprint 2 | 21 | 21 | 3 | 6 |
| Sprint 3 | 18 | 18 | 1 | 6 |
| **Total** | **63** | **63** | **6** | **18** |

### Velocity promedio: **21 puntos/sprint**

### Throughput: **6 historias/sprint** (18 historias en 3 sprints)

### Participación equitativa

| Integrante | Commits | PRs | Issues creados | Reviews |
|---|---|---|---|---|
| @SantiagoGarzon | ~20 | 6 | 7 | 6 |
| @MateoBermejo | ~25 | 6 | 6 | 6 |
| @JhonatanPedroza | ~18 | 6 | 5 | 6 |

---

## 💡 Lecciones Aprendidas del Equipo

1. **Proteger `main` desde el día 1** — Un merge accidental a `main` sin review causó downtime temporal
2. **El Dockerfile debe usar `$PORT`** — Cloud Run asigna el puerto dinámicamente; hardcodear `8000` rompe el servicio
3. **CORS tiene dos capas en GCP** — El portal de GCP Y el middleware de FastAPI; deben estar en sincronía
4. **La rama de desarrollo salva vidas** — `development` como integración evitó 3 conflictos potenciales en `main`
5. **Documentar durante el desarrollo** — Escribir docs al final toma el doble de tiempo y se olvidan detalles importantes
6. **Cloud Run es más económico que App Service** — Solo cobra por requests activos, ideal para proyectos académicos

---

## 🔮 Mejoras Futuras

- [ ] Implementar autenticación JWT para proteger los endpoints
- [ ] Agregar pruebas automatizadas con `pytest` en el pipeline CI/CD
- [ ] Configurar dominio personalizado con Cloud CDN para el frontend
- [ ] Implementar paginación en `GET /api/vehiculos` para grandes volúmenes
- [ ] Dashboard de métricas con Cloud Monitoring y alertas automáticas
- [ ] Dockerizar también el frontend con Nginx para mayor control
