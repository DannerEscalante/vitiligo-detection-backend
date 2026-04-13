import tensorflow as tf
import numpy as np
import cv2
from tensorflow.keras.applications.efficientnet import preprocess_input

MODEL_PATH = "models_ml/modelo_vitiligo_final.keras"

modelo = None


def cargar_modelo():
    global modelo
    if modelo is None:
        modelo = tf.keras.models.load_model(MODEL_PATH, compile=False)
    return modelo


def predecir_imagen(file):
    model = cargar_modelo()

    # Leer imagen como en colab
    file_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        raise Exception("No se pudo leer la imagen")

    # Convertir a RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Resize EXACTO
    img_resized = cv2.resize(img_rgb, (224, 224))

    # Preprocesamiento EXACTO del colab
    img_input = preprocess_input(
        np.expand_dims(img_resized, axis=0).astype(np.float32)
    )

    # Predicción
    prob = float(model.predict(img_input, verbose=0)[0][0])

    # Lógica EXACTA del colab
    umbral = 0.5

    if prob >= umbral:
        diagnostico = "VITÍLIGO DETECTADO"
        confianza = prob * 100
    else:
        diagnostico = "PIEL SANA (NO VITÍLIGO)"
        confianza = (1.0 - prob) * 100

    return {
        "probabilidad": prob,
        "diagnostico": diagnostico,
        "confianza": confianza
    }