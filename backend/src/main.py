from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    Header,
    Response
)

from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    generate_latest
)

import time

from . import models, schemas
from .database import SessionLocal, engine

# Crear tablas automáticamente
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Autolavado",
    description="Sistema CRUD de gestión de vehículos y servicios",
    version="2.0.0",
)

# ==========================
# CORS
# ==========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# MÉTRICAS PROMETHEUS
# ==========================
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests"
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Request Duration"
)

ACTIVE_VEHICLES = Gauge(
    "active_vehicles",
    "Cantidad de vehículos registrados"
)

# ==========================
# API KEY
# ==========================
API_KEY = "autolavado2026"


def verify_api_key(
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="API Key inválida"
        )


# ==========================
# DB SESSION
# ==========================
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ==========================
# HEALTH CHECK
# ==========================
@app.get("/", tags=["Health"])
def root():
    return {
        "status": "ok",
        "app": "Autolavado",
        "environment": "Local Docker"
    }


# ==========================
# MÉTRICAS
# ==========================
@app.get("/metrics", tags=["Monitoring"])
def metrics():
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )


# ==========================
# VEHÍCULOS
# ==========================
@app.get(
    "/api/vehiculos",
    response_model=List[schemas.VehiculoOut],
    tags=["Vehículos"]
)
def listar_vehiculos(
    db: Session = Depends(get_db)
):
    inicio = time.time()

    REQUEST_COUNT.inc()

    vehiculos = (
        db.query(models.Vehiculo)
        .order_by(models.Vehiculo.id.desc())
        .all()
    )

    ACTIVE_VEHICLES.set(
        len(vehiculos)
    )

    REQUEST_LATENCY.observe(
        time.time() - inicio
    )

    return vehiculos


@app.get(
    "/api/vehiculos/search",
    response_model=List[schemas.VehiculoOut],
    tags=["Vehículos"]
)
def buscar_vehiculos(
    placa: str,
    db: Session = Depends(get_db)
):
    return (
        db.query(models.Vehiculo)
        .filter(
            models.Vehiculo.placa.ilike(
                f"%{placa}%"
            )
        )
        .all()
    )


@app.get(
    "/api/vehiculos/{vehiculo_id}",
    response_model=schemas.VehiculoOut,
    tags=["Vehículos"]
)
def obtener_vehiculo(
    vehiculo_id: int,
    db: Session = Depends(get_db)
):
    vehiculo = (
        db.query(models.Vehiculo)
        .filter(
            models.Vehiculo.id == vehiculo_id
        )
        .first()
    )

    if not vehiculo:
        raise HTTPException(
            status_code=404,
            detail="Vehículo no encontrado"
        )

    return vehiculo


@app.post(
    "/api/vehiculos",
    response_model=schemas.VehiculoOut,
    status_code=201,
    tags=["Vehículos"]
)
def crear_vehiculo(
    vehiculo: schemas.VehiculoCreate,
    db: Session = Depends(get_db),
    api=Depends(verify_api_key)
):
    existente = (
        db.query(models.Vehiculo)
        .filter(
            models.Vehiculo.placa == vehiculo.placa
        )
        .first()
    )

    if existente:
        raise HTTPException(
            status_code=400,
            detail="La placa ya está registrada"
        )

    nuevo = models.Vehiculo(
        **vehiculo.model_dump()
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


@app.put(
    "/api/vehiculos/{vehiculo_id}",
    response_model=schemas.VehiculoOut,
    tags=["Vehículos"]
)
def actualizar_vehiculo(
    vehiculo_id: int,
    datos: schemas.VehiculoCreate,
    db: Session = Depends(get_db),
    api=Depends(verify_api_key)
):
    vehiculo = (
        db.query(models.Vehiculo)
        .filter(
            models.Vehiculo.id == vehiculo_id
        )
        .first()
    )

    if not vehiculo:
        raise HTTPException(
            status_code=404,
            detail="Vehículo no encontrado"
        )

    for campo, valor in datos.model_dump().items():
        setattr(
            vehiculo,
            campo,
            valor
        )

    db.commit()
    db.refresh(vehiculo)

    return vehiculo


@app.delete(
    "/api/vehiculos/{vehiculo_id}",
    status_code=204,
    tags=["Vehículos"]
)
def eliminar_vehiculo(
    vehiculo_id: int,
    db: Session = Depends(get_db),
    api=Depends(verify_api_key)
):
    vehiculo = (
        db.query(models.Vehiculo)
        .filter(
            models.Vehiculo.id == vehiculo_id
        )
        .first()
    )

    if not vehiculo:
        raise HTTPException(
            status_code=404,
            detail="Vehículo no encontrado"
        )

    db.delete(vehiculo)
    db.commit()

    return None


# ==========================
# SERVICIOS
# ==========================
@app.get(
    "/api/servicios",
    response_model=List[schemas.ServicioOut],
    tags=["Servicios"]
)
def listar_servicios(
    db: Session = Depends(get_db)
):
    return (
        db.query(models.Servicio)
        .order_by(models.Servicio.id.desc())
        .all()
    )


@app.post(
    "/api/servicios",
    response_model=schemas.ServicioOut,
    status_code=201,
    tags=["Servicios"]
)
def crear_servicio(
    servicio: schemas.ServicioCreate,
    db: Session = Depends(get_db),
    api=Depends(verify_api_key)
):
    vehiculo = (
        db.query(models.Vehiculo)
        .filter(
            models.Vehiculo.id == servicio.vehiculo_id
        )
        .first()
    )

    if not vehiculo:
        raise HTTPException(
            status_code=400,
            detail="El vehiculo_id no existe"
        )

    nuevo = models.Servicio(
        **servicio.model_dump()
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


@app.delete(
    "/api/servicios/{servicio_id}",
    status_code=204,
    tags=["Servicios"]
)
def eliminar_servicio(
    servicio_id: int,
    db: Session = Depends(get_db),
    api=Depends(verify_api_key)
):
    servicio = (
        db.query(models.Servicio)
        .filter(
            models.Servicio.id == servicio_id
        )
        .first()
    )

    if not servicio:
        raise HTTPException(
            status_code=404,
            detail="Servicio no encontrado"
        )

    db.delete(servicio)
    db.commit()

    return None


# ==========================
# RELACIÓN
# ==========================
@app.get(
    "/api/vehiculos/{vehiculo_id}/servicios",
    response_model=List[schemas.ServicioOut],
    tags=["Relación"]
)
def servicios_por_vehiculo(
    vehiculo_id: int,
    db: Session = Depends(get_db)
):
    vehiculo = (
        db.query(models.Vehiculo)
        .filter(
            models.Vehiculo.id == vehiculo_id
        )
        .first()
    )

    if not vehiculo:
        raise HTTPException(
            status_code=404,
            detail="Vehículo no encontrado"
        )

    return (
        db.query(models.Servicio)
        .filter(
            models.Servicio.vehiculo_id == vehiculo_id
        )
        .order_by(
            models.Servicio.fecha_servicio.desc()
        )
        .all()
    )