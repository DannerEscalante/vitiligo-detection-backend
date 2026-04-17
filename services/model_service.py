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
        try:
            modelo = construir_modelo()
            modelo.load_weights(MODEL_WEIGHTS)
        except Exception:
            raise Exception("Error cargando el modelo")
    return modelo


def predecir_imagen(ruta_imagen):
    from PIL import Image

    
    model = cargar_modelo()

    img = Image.open(ruta_imagen).convert("RGB")
    img = img.resize((224, 224))

    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    pred = model.predict(img_array)[0][0]

    if pred >= 0.5:
        diagnostico = "VITÍLIGO DETECTADO"
        confianza = float(pred * 100)
    else:
        diagnostico = "NO VITÍLIGO"
        confianza = float((1 - pred) * 100)

    return {
        "probabilidad": float(pred),
        "diagnostico": diagnostico,
        "confianza": confianza
    }