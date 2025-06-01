from fastapi import FastAPI
from services import crud
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/api/eventos")
def get_eventos():
    eventos = crud.listar_eventos()
    return [{
        "id": e.id,
        "nombre_evento": e.nombre_evento,
        "descripcion": e.descripcion,
        "fecha_evento": e.fecha_evento.isoformat(),
        "lugar": e.lugar,
        "precio": float(e.precio),
        "aforo": e.aforo
    } for e in eventos]
