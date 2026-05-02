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
    tratamiento_id: int = None,
    guardar: bool = True,
    imagen: UploadFile = File(...),
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    try:
        if not imagen or imagen.filename == "":
            raise HTTPException(status_code=400, detail="Imagen inválida")

        if not imagen.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Debe ser una imagen")

        contenido = await imagen.read()

        if len(contenido) > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Máx 5MB")

        paciente = db.query(Paciente).filter(
            Paciente.usuario_id == int(usuario_id)
        ).first()

        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")

        # guardar temporal SIEMPRE (para IA)
        filename = f"{uuid.uuid4()}.jpg"
        file_path = f"{UPLOAD_DIR}/{filename}"

        with open(file_path, "wb") as f:
            f.write(contenido)

        # predicción IA
        resultado = predecir_imagen(file_path)

        # SI NO QUIERE GUARDAR → SOLO DEVOLVER
        if not guardar:
            return {
                "prediccion_id": None,
                "resultado": resultado["diagnostico"],
                "confianza": resultado["confianza"]
            }

        # AQUÍ RECIÉN SE GUARDA EN DB

        nueva_imagen = Imagen(
            paciente_id=paciente.id,
            url_imagen=file_path,
            fecha=datetime.utcnow()
        )
        db.add(nueva_imagen)
        db.commit()
        db.refresh(nueva_imagen)

        nueva_prediccion = Prediccion(
            tratamiento_id=tratamiento_id,
            resultado=resultado["diagnostico"],
            confianza=resultado["confianza"]
        )

        db.add(nueva_prediccion)
        db.commit()
        db.refresh(nueva_prediccion)

        nueva_imagen.prediccion_id = nueva_prediccion.id
        db.commit()

        return {
            "prediccion_id": nueva_prediccion.id,
            "resultado": resultado["diagnostico"],
            "confianza": resultado["confianza"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
@router.post("/predict-inicial")
async def predict_inicial(
    imagen: UploadFile = File(...),
    usuario_id: str = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    try:
        if not imagen or imagen.filename == "":
            raise HTTPException(status_code=400, detail="Imagen inválida")

        if not imagen.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Debe ser imagen")

        contenido = await imagen.read()

        paciente = db.query(Paciente).filter(
            Paciente.usuario_id == int(usuario_id)
        ).first()

        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")

        # guardar imagen
        filename = f"{uuid.uuid4()}.jpg"
        file_path = f"{UPLOAD_DIR}/{filename}"

        with open(file_path, "wb") as f:
            f.write(contenido)

        nueva_imagen = Imagen(
            paciente_id=paciente.id,
            url_imagen=file_path,
            fecha=datetime.utcnow()
        )
        db.add(nueva_imagen)
        db.commit()
        db.refresh(nueva_imagen)

        # predicción
        resultado = predecir_imagen(file_path)

        nueva_prediccion = Prediccion(
            tratamiento_id=None,  
            resultado=resultado["diagnostico"],
            confianza=resultado["confianza"]
        )

        db.add(nueva_prediccion)
        db.commit()
        db.refresh(nueva_prediccion)

        # relación
        nueva_imagen.prediccion_id = nueva_prediccion.id
        db.commit()

        return {
            "prediccion_id": nueva_prediccion.id,
            "resultado": resultado["diagnostico"],
            "confianza": resultado["confianza"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))   
    
    
    
    
    