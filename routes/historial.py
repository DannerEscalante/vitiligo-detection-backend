from fastapi import APIRouter, Depends, HTTPException
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
    
    paciente = db.query(Paciente).filter(Paciente.usuario_id == int(usuario_id)).first()

    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    
    imagenes = db.query(Imagen).filter(Imagen.paciente_id == paciente.id).all()

    historial = []

   
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