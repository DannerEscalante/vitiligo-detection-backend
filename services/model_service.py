import tensorflow as tf
import numpy as np
import cv2
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras import layers, models

MODEL_WEIGHTS = "models_ml/pesos_vitiligo.weights.h5"

modelo = None


def construir_modelo():
    base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(224,224,3))
    base_model.trainable = False

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Dropout(0.4),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(1, activation='sigmoid')
    ])

    return model


def cargar_modelo():
    global modelo
    if modelo is None:
        modelo = construir_modelo()
        modelo.load_weights(MODEL_WEIGHTS)
    return modelo


def predecir_imagen(file):
    model = cargar_modelo()

    file.seek(0)
    file_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        raise Exception("No se pudo leer la imagen")

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_resized = cv2.resize(img_rgb, (224, 224))

    img_input = preprocess_input(
        np.expand_dims(img_resized, axis=0).astype(np.float32)
    )

    prob = float(model.predict(img_input, verbose=0)[0][0])

    if prob >= 0.5:
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