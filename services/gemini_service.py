import os
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print("GEMINI KEY:", GEMINI_API_KEY)

def generar_visual_gemini(image_path):

    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"

    response = requests.get(url)

    return response.json()