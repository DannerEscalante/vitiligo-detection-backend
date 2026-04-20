from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from core.deps import obtener_usuario_actual
from core.database import SessionLocal
from services.model_service import predecir_imagen
from models import Paciente, Imagen, Prediccion
from datetime import datetime
import shutil
import os
from fastapi import HTTPException
import uuid
from io import BytesIO

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        


filename = f"{uuid.uuid4()}.jpg"
file_path = f"{UPLOAD_DIR}/{filename}"


@router.post("/predict")
async def predict(
    imagen: UploadFile = File(...),
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    try:

        if not imagen:
            raise HTTPException(status_code=400, detail="No se envió ninguna imagen")

        if imagen.filename == "":
            raise HTTPException(status_code=400, detail="Nombre de archivo inválido")

        if not imagen.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
        
        contenido = await imagen.read()

        if len(contenido) > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="La imagen es demasiado grande (máx 5MB)")

        
        imagen.file = BytesIO(contenido)


        paciente = db.query(Paciente).filter(Paciente.usuario_id == int(usuario_id)).first()

        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")

        file_path = f"{UPLOAD_DIR}/{imagen.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(imagen.file, buffer)


        nueva_imagen = Imagen(
            paciente_id=paciente.id,
            url_imagen=file_path,
            fecha_subida=datetime.utcnow()
        )
        db.add(nueva_imagen)
        db.commit()
        db.refresh(nueva_imagen)


        resultado = predecir_imagen(file_path)


        nueva_prediccion = Prediccion(
            imagen_id=nueva_imagen.id,
            resultado=resultado["diagnostico"],
            confianza=resultado["confianza"],
            fecha_prediccion=datetime.utcnow()
        )
        db.add(nueva_prediccion)
        db.commit()


        return {
            "usuario_id": usuario_id,
            **resultado
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))