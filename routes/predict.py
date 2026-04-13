from fastapi import APIRouter, Depends, File, UploadFile
from core.deps import obtener_usuario_actual
from services.model_service import predecir_imagen

router = APIRouter()


@router.post("/predict")
async def predict(
    imagen: UploadFile = File(...),
    usuario_id: str = Depends(obtener_usuario_actual)
):
    try:
        resultado = predecir_imagen(imagen.file)

        return {
            "usuario_id": usuario_id,
            **resultado
        }

    except Exception as e:
        return {
            "error": str(e)
        }