"""
main.py — API REST Autolavado
Backend: Azure App Service | DB: GCP Cloud SQL (PostgreSQL)
Endpoints mínimos requeridos por el documento de actividad.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Autolavado",
    description="Sistema CRUD de gestión de vehículos y servicios de autolavado",
    version="1.0.0",
)

# ── CORS (en producción limitar al dominio del frontend en Azure) ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ════════════════════════════════════════════════════════════════
#  VEHÍCULOS  — entidad1 (CRUD completo)
# ════════════════════════════════════════════════════════════════

@app.get("/api/vehiculos", response_model=List[schemas.VehiculoOut], tags=["Vehículos"])
def listar_vehiculos(db: Session = Depends(get_db)):
    """GET /api/vehiculos — Lista todos los vehículos registrados."""
    return db.query(models.Vehiculo).order_by(models.Vehiculo.id.desc()).all()


@app.get("/api/vehiculos/{vehiculo_id}", response_model=schemas.VehiculoOut, tags=["Vehículos"])
def obtener_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    """GET /api/vehiculos/{id} — Obtiene un vehículo por ID."""
    v = db.query(models.Vehiculo).filter(models.Vehiculo.id == vehiculo_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return v


@app.post("/api/vehiculos", response_model=schemas.VehiculoOut, status_code=201, tags=["Vehículos"])
def crear_vehiculo(vehiculo: schemas.VehiculoCreate, db: Session = Depends(get_db)):
    """POST /api/vehiculos — Registra un nuevo vehículo."""
    existente = db.query(models.Vehiculo).filter(models.Vehiculo.placa == vehiculo.placa).first()
    if existente:
        raise HTTPException(status_code=400, detail=f"La placa {vehiculo.placa} ya está registrada")
    db_v = models.Vehiculo(**vehiculo.model_dump())
    db.add(db_v)
    db.commit()
    db.refresh(db_v)
    return db_v


@app.put("/api/vehiculos/{vehiculo_id}", response_model=schemas.VehiculoOut, tags=["Vehículos"])
def actualizar_vehiculo(vehiculo_id: int, datos: schemas.VehiculoCreate, db: Session = Depends(get_db)):
    """PUT /api/vehiculos/{id} — Actualiza los datos de un vehículo."""
    v = db.query(models.Vehiculo).filter(models.Vehiculo.id == vehiculo_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(v, campo, valor)
    db.commit()
    db.refresh(v)
    return v


@app.delete("/api/vehiculos/{vehiculo_id}", status_code=204, tags=["Vehículos"])
def eliminar_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    """DELETE /api/vehiculos/{id} — Elimina un vehículo y sus servicios."""
    v = db.query(models.Vehiculo).filter(models.Vehiculo.id == vehiculo_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    db.delete(v)
    db.commit()


# ════════════════════════════════════════════════════════════════
#  SERVICIOS  — entidad2
# ════════════════════════════════════════════════════════════════

@app.get("/api/servicios", response_model=List[schemas.ServicioOut], tags=["Servicios"])
def listar_servicios(db: Session = Depends(get_db)):
    """GET /api/servicios — Lista todos los servicios."""
    return db.query(models.Servicio).order_by(models.Servicio.id.desc()).all()


@app.post("/api/servicios", response_model=schemas.ServicioOut, status_code=201, tags=["Servicios"])
def crear_servicio(servicio: schemas.ServicioCreate, db: Session = Depends(get_db)):
    """POST /api/servicios — Registra un nuevo servicio para un vehículo."""
    v = db.query(models.Vehiculo).filter(models.Vehiculo.id == servicio.vehiculo_id).first()
    if not v:
        raise HTTPException(status_code=400, detail="El vehiculo_id no existe")
    db_s = models.Servicio(**servicio.model_dump())
    db.add(db_s)
    db.commit()
    db.refresh(db_s)
    return db_s


@app.delete("/api/servicios/{servicio_id}", status_code=204, tags=["Servicios"])
def eliminar_servicio(servicio_id: int, db: Session = Depends(get_db)):
    """DELETE /api/servicios/{id} — Cancela/elimina un servicio."""
    s = db.query(models.Servicio).filter(models.Servicio.id == servicio_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    db.delete(s)
    db.commit()


# ════════════════════════════════════════════════════════════════
#  RELACIÓN — servicios de un vehículo específico
# ════════════════════════════════════════════════════════════════

@app.get(
    "/api/vehiculos/{vehiculo_id}/servicios",
    response_model=List[schemas.ServicioOut],
    tags=["Relación"],
)
def servicios_por_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    """GET /api/vehiculos/{id}/servicios — Historial de servicios de un vehículo."""
    v = db.query(models.Vehiculo).filter(models.Vehiculo.id == vehiculo_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return (
        db.query(models.Servicio)
        .filter(models.Servicio.vehiculo_id == vehiculo_id)
        .order_by(models.Servicio.fecha_servicio.desc())
        .all()
    )


# ── Health check ──────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "app": "API Autolavado", "cloud": "Azure App Service + GCP Cloud SQL"}
