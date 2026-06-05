# Security Report

## Vulnerabilidades Identificadas

### 1. Acceso no autorizado a operaciones críticas

**Descripción:**
Los endpoints de creación, actualización y eliminación podrían ser utilizados por cualquier usuario si no existe autenticación.

**Impacto:**
Modificación o eliminación indebida de información almacenada.

---

### 2. Comunicación sin HTTPS

**Descripción:**
Actualmente el sistema opera en entorno local mediante HTTP.

**Impacto:**
La información podría ser interceptada en un entorno productivo.

---

### 3. Exposición de métricas

**Descripción:**
El endpoint `/metrics` se encuentra disponible para Prometheus.

**Impacto:**
Un atacante podría obtener información sobre el comportamiento del sistema.

---

## Medidas Implementadas

### Vulnerabilidad 1

Se implementó autenticación mediante API Key utilizando el encabezado:

```http
x-api-key: autolavado2026
```

Protegiendo:

- POST
- PUT
- DELETE

---

### Vulnerabilidad 2

El sistema se encuentra desplegado únicamente en ambiente académico local.

Se documenta como mejora futura la implementación de HTTPS.

---

### Vulnerabilidad 3

Las métricas se utilizan exclusivamente para monitoreo mediante Prometheus y Grafana.

---

## Medidas Pendientes

### HTTPS

Implementar certificados TLS para cifrar el tráfico.

### JWT

Reemplazar API Key por autenticación basada en tokens.

### Roles

Implementar niveles de acceso:

- Administrador
- Operador
- Consulta

### Rate Limiting

Limitar la cantidad de solicitudes por cliente.

---

## Plan de Respuesta a Incidentes

Si se detecta acceso no autorizado:

1. Revocar inmediatamente las credenciales comprometidas.
2. Revisar los registros de acceso.
3. Identificar los recursos afectados.
4. Restaurar información desde respaldo si es necesario.
5. Generar nuevas credenciales.
6. Documentar el incidente y aplicar medidas preventivas.

---

## Conclusiones

Se implementaron mecanismos básicos de autenticación y monitoreo adecuados para los objetivos académicos del proyecto. Existen oportunidades de mejora relacionadas con HTTPS, JWT y control granular de acceso.