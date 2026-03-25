#!/usr/bin/env python3
"""test_connection.py — Script para validar la conexión a la base de datos GCP Cloud SQL"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

try:
    from src.database import engine, SessionLocal

    # Intentar conectar
    with engine.connect() as connection:
        result = connection.execute("SELECT 1 as test")
        print("✅ Conexión exitosa a la base de datos GCP Cloud SQL!")
        print(f"Resultado de prueba: {result.fetchone()}")

    # Probar sesión
    db = SessionLocal()
    db.close()
    print("✅ Sesión de base de datos creada y cerrada correctamente.")

except Exception as e:
    print(f"❌ Error de conexión: {e}")
    print("\nPosibles causas:")
    print("- Credenciales incorrectas en .env")
    print("- Instancia de GCP SQL no accesible (IP no autorizada)")
    print("- Puerto o host incorrecto")
    print("- Base de datos no existe")
    print("\nVerifica:")
    print("- Que DATABASE_URL esté configurada correctamente")
    print("- Que la IP de tu máquina esté autorizada en GCP SQL")
    print("- Que uses Cloud SQL Auth Proxy si es necesario")