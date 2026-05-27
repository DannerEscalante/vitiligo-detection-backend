import os
import requests
import base64



GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print("GEMINI KEY:", GEMINI_API_KEY)

def generar_visual_gemini(image_path):

    with open(image_path, "rb") as img_file:
        image_base64 = base64.b64encode(
            img_file.read()
        ).decode("utf-8")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={GEMINI_API_KEY}"

    prompt = """
    Resalta suavemente las posibles zonas despigmentadas compatibles con vitiligo usando un overlay rojo translúcido.
    
    Mantén intacta la anatomía, textura y colores reales de la piel.
    
    No modifiques el fondo.
    
    No generes una nueva imagen.
    
    Solo añade resaltado visual médico sutil sobre posibles manchas de vitiligo.
    """

    body = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    },
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_base64
                        }
                    }
                ]
            }
        ]
    }

    response = requests.post(
        url,
        json=body
    )

    return response.json()