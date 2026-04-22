"""database.py — Conexión SQLAlchemy — GCP Cloud SQL"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Lee desde variable de entorno.
# Formato Cloud Run (socket):
# postgresql://user:pass@/db?host=/cloudsql/PROJECT:REGION:INSTANCE
# Formato local (IP pública):  postgresql://user:pass@IP:5432/db
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/autolavado_db"  # fallback local
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
