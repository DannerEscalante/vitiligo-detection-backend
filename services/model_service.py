import numpy as np
import cv2
import os

from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras import layers, models, regularizers

# -----------------------------
# 🔹 RUTA DE PESOS
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEIGHTS_PATH = os.path.join(BASE_DIR, "..", "models_ml", "modelo_pesos.weights.h5")

# -----------------------------
# 🔹 CONSTRUIR MODELO (MISMA ARQUITECTURA QUE ENTRENAMIENTO)
# -----------------------------
def construir_modelo():
    base_model = EfficientNetB0(
        weights="imagenet",
        include_top=False,
        input_shape=(224, 224, 3)
    )

    base_model.trainable = False

    x = base_model.output
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.6)(x)

    x = layers.Dense(
        128,
        activation="relu",
        kernel_regularizer=regularizers.l2(0.02)
    )(x)

    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.5)(x)

    outputs = layers.Dense(1, activation="sigmoid")(x)

    model = models.Model(inputs=base_model.input, outputs=outputs)

    return model

# -----------------------------
# 🔹 CARGAR MODELO UNA SOLA VEZ
# -----------------------------
model = construir_modelo()
model.load_weights(WEIGHTS_PATH)

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
    img = cv2.imread(path)

    if img is None:
        raise Exception("No se pudo leer la imagen")

    # 🔥 MISMO PIPELINE QUE ENTRENAMIENTO
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