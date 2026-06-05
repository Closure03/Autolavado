import requests

for i in range(500):
    requests.get(
        "http://localhost:8000/api/vehiculos"
    )

print("Tráfico generado correctamente")