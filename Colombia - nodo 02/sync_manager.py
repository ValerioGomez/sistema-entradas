import requests
import time
from services import crud
import json

with open("services/config.json") as f:
    config = json.load(f)

NODOS = config.get("nodos", [])

def sincronizar_datos():
    for nodo in NODOS:
        try:
            url = f"http://{nodo}/api/eventos"
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                eventos_remotos = resp.json()
                for ev in eventos_remotos:
                    try:
                        # Insertar evento solo si no existe (ejemplo simple)
                        crud.crear_evento(
                            ev['nombre_evento'],
                            ev.get('descripcion', ''),
                            ev['fecha_evento'],
                            ev.get('lugar', ''),
                            ev['precio'],
                            ev['aforo']
                        )
                    except Exception:
                        # Si ya existe, ignorar o actualizar (según lógica)
                        pass
        except Exception as e:
            print(f"No se pudo conectar con nodo {nodo}: {e}")

def sincronizar_datos_periodicamente(interval=60):
    while True:
        sincronizar_datos()
        time.sleep(interval)
