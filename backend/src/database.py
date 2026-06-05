"""database.py — Conexión local PostgreSQL"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://postgres:123456@postgres:5432/autolavado"

engine = create_engine(
DATABASE_URL,
pool_pre_ping=True
)

SessionLocal = sessionmaker(
autocommit=False,
autoflush=False,
bind=engine
)

Base = declarative_base()
