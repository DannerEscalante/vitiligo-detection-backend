from fastapi import APIRouter, UploadFile, File
import shutil
import os

from services.gemini_service import generar_visual_gemini

router = APIRouter()

TEMP_DIR = "temp_visuals"

@router.post("/test-gemini")

async def test_gemini(
    file: UploadFile = File(...)
):

    os.makedirs(TEMP_DIR, exist_ok=True)

    filepath = os.path.join(
        TEMP_DIR,
        file.filename
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = generar_visual_gemini(filepath)

    return result