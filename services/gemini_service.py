import os
import requests
import base64
import json

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print("GEMINI KEY:", GEMINI_API_KEY)

def detectar_regiones_vitiligo(image_path):

    with open(image_path, "rb") as img_file:
        image_base64 = base64.b64encode(
            img_file.read()
        ).decode("utf-8")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

    prompt = """
    Analiza la imagen dermatológica.

    Detecta posibles zonas compatibles con vitiligo.

    Devuelve únicamente un JSON válido.

    Usa coordenadas normalizadas entre 0 y 1.

    Formato:

    {
      "regions": [
        {
          "x": 0.1,
          "y": 0.2,
          "width": 0.3,
          "height": 0.4
        }
      ]
    }

    NO expliques nada.
    NO uses markdown.
    SOLO devuelve JSON.
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

    result = response.json()

    try:

        text = result["candidates"][0]["content"]["parts"][0]["text"]

        text = text.replace("```json", "")
        text = text.replace("```", "")

        return json.loads(text)

    except Exception as e:

        return {
            "error": str(e),
            "raw": result
        }