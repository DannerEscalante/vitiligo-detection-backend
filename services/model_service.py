import tensorflow as tf
import numpy as np
from PIL import Image

MODEL_PATH = "models_ml/modelo_vitiligo_final.keras"

modelo = None  # modelo global (no se carga al inicio)


def cargar_modelo():
    global modelo
    if modelo is None:
        modelo = tf.keras.models.load_model(MODEL_PATH, compile=False)
    return modelo


def predecir_imagen(file):
    model = cargar_modelo()

    img = Image.open(file).convert("RGB")
    img = img.resize((224, 224))

    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    pred = model.predict(img_array)[0][0]

    return float(pred)