import numpy as np
import cv2
import os
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import preprocess_input

# -----------------------------
# 🔹 RUTA DEL MODELO
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models_ml", "modelo_exportado")

modelo = None

# -----------------------------
# 🔹 CARGAR MODELO (KERAS 3)
# -----------------------------
def cargar_modelo():
    global modelo
    if modelo is None:
        modelo = tf.keras.layers.TFSMLayer(
            MODEL_PATH,
            call_endpoint="serving_default"
        )
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

    # 🔥 IMPORTANTE: mantener BGR aquí
    # porque la máscara usa HSV desde BGR

    # 1. máscara primero (como en colab)
    img = aplicar_mascara_piel(img)

    # 2. luego contraste
    img = mejorar_contraste(img)

    # 3. resize
    img = cv2.resize(img, (224, 224))

    # 🔥 AHORA sí convertir a RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img = np.array(img, dtype=np.float32)

    # 4. preprocess
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)

    pred = model(img)

    if isinstance(pred, dict):
        pred = list(pred.values())[0]

    pred = pred.numpy()[0][0]

    print("PRED BACKEND:", pred)

    return {
        "diagnostico": "vitiligo" if pred > 0.5 else "no_vitiligo",
        "confianza": float(pred)
    }