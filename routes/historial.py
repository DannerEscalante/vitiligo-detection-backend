from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.deps import obtener_usuario_actual
from core.database import SessionLocal
from models import Paciente, Imagen, Prediccion

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/historial")
def obtener_historial(
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    # 🔹 1. Obtener paciente
    paciente = db.query(Paciente).filter(Paciente.usuario_id == int(usuario_id)).first()

    if not paciente:
        return {"error": "Paciente no encontrado"}

    # 🔹 2. Obtener imágenes del paciente
    imagenes = db.query(Imagen).filter(Imagen.paciente_id == paciente.id).all()

    historial = []

    # 🔹 3. Recorrer imágenes y obtener predicciones
    for img in imagenes:
        predicciones = db.query(Prediccion).filter(Prediccion.imagen_id == img.id).all()

        for pred in predicciones:
            historial.append({
                "imagen": img.url_imagen,
                "resultado": pred.resultado,
                "confianza": pred.confianza,
                "fecha": pred.fecha_prediccion
            })

    return historial