"""models.py — Modelos SQLAlchemy: Autolavado"""

from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id          = Column(Integer, primary_key=True, index=True)
    placa       = Column(String(10),  nullable=False, unique=True)
    marca       = Column(String(60),  nullable=False)
    modelo      = Column(String(60),  nullable=False)
    anio        = Column(Integer)
    color       = Column(String(40))
    tipo        = Column(String(30),  nullable=False, default="sedan")
    propietario = Column(String(120), nullable=False)
    telefono    = Column(String(20))
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(DateTime(timezone=True), onupdate=func.now())

    servicios = relationship("Servicio", back_populates="vehiculo", cascade="all, delete")


class Servicio(Base):
    __tablename__ = "servicios"

    id             = Column(Integer,      primary_key=True, index=True)
    vehiculo_id    = Column(Integer,      ForeignKey("vehiculos.id"), nullable=False)
    tipo_servicio  = Column(String(60),   nullable=False, default="lavado_basico")
    precio         = Column(Numeric(10,2),nullable=False)
    estado         = Column(String(20),   nullable=False, default="pendiente")
    observaciones  = Column(Text)
    fecha_servicio = Column(DateTime(timezone=True), server_default=func.now())
    created_at     = Column(DateTime(timezone=True), server_default=func.now())

    vehiculo = relationship("Vehiculo", back_populates="servicios")
