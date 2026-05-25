import numpy as np
import cv2
import os
import tensorflow as tf
import base64
from tensorflow.keras.applications.efficientnet import preprocess_input

# -----------------------------
# RUTA DEL MODELO
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models_ml", "modelo_exportado")
GRADCAM_MODEL_PATH = os.path.join(
    BASE_DIR,
    "..",
    "models_ml",
    "modelo_gradcam_limpio.h5"
)

modelo = None
modelo_gradcam = None

# -----------------------------
# CARGAR MODELO
# -----------------------------
def cargar_modelo():

    global modelo
    global modelo_gradcam

    #prueba
    # Modelo principal (TFSMLayer)
    if modelo is None:

        modelo = tf.keras.layers.TFSMLayer(
            MODEL_PATH,
            call_endpoint="serving_default"
        )

    # Modelo GradCAM (.keras)
    if modelo_gradcam is None:

        modelo_gradcam = tf.keras.models.load_model(
            GRADCAM_MODEL_PATH,
            compile=False,
            safe_mode=False
        )

    return modelo, modelo_gradcam

# -----------------------------
# CLAHE
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



# -----------------------------
# MÁSCARA PIEL
# -----------------------------
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
# GENERAR VISUALIZACIÓN IA
# -----------------------------
def generar_overlay(original_img, heatmap, pred):

    heatmap_uint8 = np.uint8(255 * heatmap)

    heatmap_blur = cv2.GaussianBlur(
        heatmap_uint8,
        (25,25),
        0
    )

    threshold = 140

    filtered_heatmap = np.where(
        heatmap_blur > threshold,
        heatmap_blur,
        0
    ).astype(np.uint8)

    color_mask = np.zeros_like(original_img)

    # VITILIGO
    if pred >= 0.5:

        color_mask[:, :, 0] = filtered_heatmap

    # NO VITILIGO
    else:

        color_mask[:, :, 1] = heatmap_blur

    result_img = cv2.addWeighted(
        original_img,
        0.75,
        color_mask,
        0.4,
        0
    )

    return result_img

# -----------------------------
# GENERAR GRADCAM
# -----------------------------
def generar_gradcam(model, img_array, original_img):

    base_model = model.layers[0]

    last_conv_layer = base_model.get_layer("top_conv")

    grad_model = tf.keras.models.Model(
        inputs=base_model.input,
        outputs=[
            last_conv_layer.output,
            base_model.output
        ]
    )

    with tf.GradientTape() as tape:

        conv_outputs, predictions = grad_model(img_array)

        loss = tf.reduce_mean(predictions)

    grads = tape.gradient(loss, conv_outputs)

    pooled_grads = tf.reduce_mean(
        grads,
        axis=(0,1,2)
    )

    conv_outputs = conv_outputs[0]

    heatmap = tf.reduce_sum(
        conv_outputs * pooled_grads,
        axis=-1
    )

    heatmap = tf.maximum(heatmap, 0)

    heatmap /= tf.math.reduce_max(heatmap)

    heatmap = heatmap.numpy()

    heatmap = cv2.resize(
        heatmap,
        (original_img.shape[1], original_img.shape[0])
    )

    return heatmap

# -----------------------------
# CONVERTIR A BASE64
# -----------------------------
def image_to_base64(img_rgb):

    img_bgr = cv2.cvtColor(
        img_rgb,
        cv2.COLOR_RGB2BGR
    )

    _, buffer = cv2.imencode(".jpg", img_bgr)

    return base64.b64encode(buffer).decode("utf-8")

# -----------------------------
# FUNCIÓN PRINCIPAL
# -----------------------------
def predecir_imagen(path):

    model, gradcam_model = cargar_modelo()

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

    # -----------------------------
    # GRADCAM
    # -----------------------------
    heatmap = generar_gradcam(
        gradcam_model,
        img_batch,
        img_resized
    )

    overlay = generar_overlay(
        img_resized,
        heatmap,
        pred
    )

    overlay_base64 = image_to_base64(overlay)

    # -----------------------------
    # RESULTADO
    # -----------------------------
    if pred >= 0.5:

        diagnostico = "vitiligo"
        confianza = float(pred)

    else:

        diagnostico = "no_vitiligo"
        confianza = float(1 - pred)

    return {
        "diagnostico": diagnostico,
        "confianza": confianza,
        "imagen_gradcam": overlay_base64
    }