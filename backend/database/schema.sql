-- ============================================================
-- SCHEMA: Sistema de Gestión de Autolavado
-- Base de datos: PostgreSQL 15 (GCP Cloud SQL)
-- Proyecto: multi-apis-cloud
-- ============================================================

DROP TABLE IF EXISTS servicios CASCADE;
DROP TABLE IF EXISTS vehiculos CASCADE;

-- ============================================================
-- TABLA: vehiculos  (entidad1 — CRUD completo)
-- ============================================================
CREATE TABLE vehiculos (
    id          SERIAL PRIMARY KEY,
    placa       VARCHAR(10)  NOT NULL UNIQUE,
    marca       VARCHAR(60)  NOT NULL,
    modelo      VARCHAR(60)  NOT NULL,
    anio        INTEGER,
    color       VARCHAR(40),
    tipo        VARCHAR(30)  NOT NULL DEFAULT 'sedan',
                             -- sedan | camioneta | moto | bus | camion
    propietario VARCHAR(120) NOT NULL,
    telefono    VARCHAR(20),
    created_at  TIMESTAMP DEFAULT NOW(),
    updated_at  TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE  vehiculos           IS 'Vehículos registrados en el autolavado';
COMMENT ON COLUMN vehiculos.placa     IS 'Placa única del vehículo (ej: ABC-123)';
COMMENT ON COLUMN vehiculos.tipo      IS 'sedan | camioneta | moto | bus | camion';

-- ============================================================
-- TABLA: servicios  (entidad2 — relacionada con vehiculos)
-- ============================================================
CREATE TABLE servicios (
    id           SERIAL PRIMARY KEY,
    vehiculo_id  INTEGER NOT NULL REFERENCES vehiculos(id) ON DELETE CASCADE,
    tipo_servicio VARCHAR(60) NOT NULL DEFAULT 'lavado_basico',
                              -- lavado_basico | lavado_completo | lavado_premium
                              -- encerado | tapizado | motor
    precio       NUMERIC(10,2) NOT NULL,
    estado       VARCHAR(20) NOT NULL DEFAULT 'pendiente',
                              -- pendiente | en_proceso | completado | cancelado
    observaciones TEXT,
    fecha_servicio TIMESTAMP DEFAULT NOW(),
    created_at   TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE  servicios              IS 'Servicios de lavado realizados a cada vehículo';
COMMENT ON COLUMN servicios.tipo_servicio IS 'Tipo de servicio de lavado';
COMMENT ON COLUMN servicios.estado        IS 'pendiente | en_proceso | completado | cancelado';

-- Índices para consultas frecuentes
CREATE INDEX idx_servicios_vehiculo ON servicios(vehiculo_id);
CREATE INDEX idx_servicios_estado   ON servicios(estado);
CREATE INDEX idx_servicios_fecha    ON servicios(fecha_servicio DESC);
