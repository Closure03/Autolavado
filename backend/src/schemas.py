"""schemas.py — Pydantic v2: Autolavado"""

from pydantic import BaseModel, field_validator
from typing import Optional, Literal
from datetime import datetime
from decimal import Decimal

TipoVehiculo   = Literal["sedan","camioneta","moto","bus","camion"]
TipoServicio   = Literal["lavado_basico","lavado_completo","lavado_premium","encerado","tapizado","motor"]
EstadoServicio = Literal["pendiente","en_proceso","completado","cancelado"]


# ── Vehículo ─────────────────────────────────────────────────────

class VehiculoCreate(BaseModel):
    placa:       str
    marca:       str
    modelo:      str
    anio:        Optional[int]  = None
    color:       Optional[str]  = None
    tipo:        TipoVehiculo   = "sedan"
    propietario: str
    telefono:    Optional[str]  = None

    @field_validator("placa")
    @classmethod
    def placa_upper(cls, v):
        return v.upper().strip()


class VehiculoOut(VehiculoCreate):
    id:         int
    created_at: Optional[datetime] = None
    model_config = {"from_attributes": True}


# ── Servicio ─────────────────────────────────────────────────────

class ServicioCreate(BaseModel):
    vehiculo_id:   int
    tipo_servicio: TipoServicio   = "lavado_basico"
    precio:        Decimal
    estado:        EstadoServicio = "pendiente"
    observaciones: Optional[str]  = None


class ServicioOut(ServicioCreate):
    id:             int
    fecha_servicio: Optional[datetime] = None
    created_at:     Optional[datetime] = None
    model_config = {"from_attributes": True}
