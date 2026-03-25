"""database.py — Configuración de la base de datos GCP Cloud SQL (PostgreSQL)"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ── Configuración de credenciales ──
# Las credenciales se obtienen de variables de entorno para seguridad.
# En desarrollo, puedes usar un archivo .env (instala python-dotenv)
# En producción, configura las variables de entorno en Azure App Service.

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurada. Define la variable de entorno DATABASE_URL.")

# ── Motor SQLAlchemy ──
engine = create_engine(DATABASE_URL, echo=True)  # echo=True para logs en desarrollo

# ── Sesión ──
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ── Base para modelos ──
Base = declarative_base()