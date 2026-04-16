from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from core.deps import obtener_usuario_actual
from core.database import SessionLocal
from services.model_service import predecir_imagen
from models import Paciente, Imagen, Prediccion
from datetime import datetime
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/predict")
async def predict(
    imagen: UploadFile = File(...),
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    try:
        # 🔹 1. Obtener paciente
        paciente = db.query(Paciente).filter(Paciente.usuario_id == int(usuario_id)).first()

        if not paciente:
            return {"error": "Paciente no encontrado"}

        # 🔹 2. Guardar imagen en servidor
        file_path = f"{UPLOAD_DIR}/{imagen.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(imagen.file, buffer)

        # 🔹 3. Guardar imagen en BD
        nueva_imagen = Imagen(
            paciente_id=paciente.id,
            url_imagen=file_path,
            fecha_subida=datetime.utcnow()
        )
        db.add(nueva_imagen)
        db.commit()
        db.refresh(nueva_imagen)

        # 🔹 4. Predecir
        resultado = predecir_imagen(file_path)

        # 🔹 5. Guardar predicción
        nueva_prediccion = Prediccion(
            imagen_id=nueva_imagen.id,
            resultado=resultado["diagnostico"],
            confianza=resultado["confianza"],
            fecha_prediccion=datetime.utcnow()
        )
        db.add(nueva_prediccion)
        db.commit()

        # 🔹 6. Respuesta
        return {
            "usuario_id": usuario_id,
            **resultado
        }

    except Exception as e:
        return {
            "error": str(e)
        }