from fastapi import APIRouter, Depends, File, UploadFile
from core.deps import obtener_usuario_actual


router = APIRouter()


@router.post("/predict")
def predict(
    imagen: UploadFile = File(...),
    usuario_id: str = Depends(obtener_usuario_actual)
):
    
    return {
        "mensaje": "Acceso permitido",
        "usuario_id": usuario_id
    }