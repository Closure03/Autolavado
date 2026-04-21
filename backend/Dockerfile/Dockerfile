# Dockerfile — AutoLavado API
# Despliegue: Google Cloud Run
FROM python:3.11-slim

# Variables de entorno de sistema
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY src/ ./src/

# ⚠️ Cloud Run asigna el puerto via variable PORT (por defecto 8080)
# Uvicorn debe escuchar en $PORT, no en 8000 fijo
CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
