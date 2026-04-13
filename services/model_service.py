import tensorflow as tf
import numpy as np
from PIL import Image

MODEL_PATH = "models_ml/modelo_vitiligo_final.keras"

modelo = tf.keras.models.load_model(MODEL_PATH, compile=False)



def predecir_imagen(file):
    img = Image.open(file).convert("RGB")
    img = img.resize((224, 224))  # depende de tu modelo

    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    pred = modelo.predict(img_array)[0][0]

    return float(pred)