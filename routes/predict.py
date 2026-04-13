from fastapi import APIRouter, Depends, File, UploadFile
from core.deps import obtener_usuario_actual
from services.model_service import predecir_imagen

router = APIRouter()

@router.post("/predict")
async def predict(
    imagen: UploadFile = File(...),
    usuario_id: str = Depends(obtener_usuario_actual)
):

    resultado = predecir_imagen(imagen.file)

    diagnostico = "vitiligo" if resultado > 0.5 else "no vitiligo"

    return {
        "usuario_id": usuario_id,
        "probabilidad": resultado,
        "diagnostico": diagnostico
    }