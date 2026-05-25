import numpy as np
import cv2
import os
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import preprocess_input

# -----------------------------
# RUTA DEL MODELO
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models_ml", "modelo_exportado")

modelo = None

# -----------------------------
# CARGAR MODELO (KERAS 3)
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
# PREPROCESAMIENTO
# -----------------------------
def mejorar_contraste(img_rgb):

    lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)

    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8,8)
    )

    l_eq = clahe.apply(l)

    lab_eq = cv2.merge((l_eq, a, b))

    return cv2.cvtColor(lab_eq, cv2.COLOR_LAB2RGB)

def aplicar_mascara_piel(img_rgb):

    img_cont = mejorar_contraste(img_rgb)

    hsv = cv2.cvtColor(img_cont, cv2.COLOR_RGB2HSV)

    lower = np.array([0, 0, 20], dtype=np.uint8)
    upper = np.array([40, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower, upper)

    kernel = np.ones((7,7), np.uint8)

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
        mask,
        connectivity=8
    )

    mask_final = np.zeros_like(mask)

    for i in range(1, num_labels):

        if stats[i, cv2.CC_STAT_AREA] > 2000:
            mask_final[labels == i] = 255

    return cv2.bitwise_and(
        img_cont,
        img_cont,
        mask=mask_final
    )

# -----------------------------
# FUNCIÓN PRINCIPAL
# -----------------------------
def predecir_imagen(path):

    model = cargar_modelo()

    img = cv2.imread(path)

    if img is None:
        raise Exception("No se pudo leer la imagen")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_resized = cv2.resize(img, (224,224))

    x_norm = preprocess_input(
        img_resized.astype(np.float32)
    )

    mean = np.array([123.68, 116.779, 103.939])

    x_rev = x_norm + mean

    x_rev = np.clip(
        x_rev,
        0,
        255
    ).astype(np.uint8)

    img_masked = aplicar_mascara_piel(x_rev)

    img_final = preprocess_input(
        img_masked.astype(np.float32)
    )

    img_batch = np.expand_dims(
        img_final,
        axis=0
    )

    pred = model(img_batch)

    if isinstance(pred, dict):
        pred = list(pred.values())[0]

    pred = pred.numpy()[0][0]

    print("PRED BACKEND:", pred)

    if pred >= 0.5:

        diagnostico = "vitiligo"
        confianza = float(pred)

    else:

        diagnostico = "no_vitiligo"
        confianza = float(1 - pred)

    return {
        "diagnostico": diagnostico,
        "confianza": confianza
    }