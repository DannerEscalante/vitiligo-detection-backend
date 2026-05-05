import numpy as np
import cv2
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input

# -----------------------------
# 🔹 RUTA DEL MODELO
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models_ml", "modelo_final_limpio_otravez.h5")

modelo = None

# -----------------------------
# 🔹 CARGAR MODELO UNA SOLA VEZ
# -----------------------------
def cargar_modelo():
    global modelo
    if modelo is None:
        modelo = load_model(MODEL_PATH, compile=False)
    return modelo

# -----------------------------
# 🔹 PREPROCESAMIENTO
# -----------------------------
def aplicar_mascara_piel(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 20, 70], dtype=np.uint8)
    upper = np.array([20, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower, upper)
    return cv2.bitwise_and(img, img, mask=mask)

def mejorar_contraste(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)

    lab = cv2.merge((l, a, b))
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

# -----------------------------
# 🔹 FUNCIÓN PRINCIPAL
# -----------------------------
def predecir_imagen(path):
    model = cargar_modelo()

    img = cv2.imread(path)

    if img is None:
        raise Exception("No se pudo leer la imagen")

    img = mejorar_contraste(img)
    img = aplicar_mascara_piel(img)

    img = cv2.resize(img, (224, 224))
    img = np.array(img, dtype=np.float32)

    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)

    pred = model.predict(img, verbose=0)[0][0]

    return {
        "diagnostico": "vitiligo" if pred > 0.5 else "no_vitiligo",
        "confianza": float(pred)
    }