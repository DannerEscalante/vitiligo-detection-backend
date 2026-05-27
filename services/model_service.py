import numpy as np
import cv2
import os
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import preprocess_input
import base64
import uuid

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
# DETECTAR ZONAS DESPIGMENTADAS
# -----------------------------
def detectar_vitiligo_visual(img_rgb):

    # CLAHE para mejorar contraste
    lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)

    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8,8)
    )

    l_eq = clahe.apply(l)

    # Suavizar
    l_blur = cv2.GaussianBlur(l_eq, (5,5), 0)

    # Adaptive Threshold
    mask_l = cv2.adaptiveThreshold(
        l_blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        51,
        -5
    )

    # Mantener solo zonas MUY claras
    _, bright_mask = cv2.threshold(
        l_blur,
        190,
        255,
        cv2.THRESH_BINARY
    )

    mask_l = cv2.bitwise_and(mask_l, bright_mask)

    # Detectar baja saturación
    hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)

    h, s, v = cv2.split(hsv)

    mask_s = cv2.threshold(
        s,
        60,
        255,
        cv2.THRESH_BINARY_INV
    )[1]

    # Combinar ambas máscaras
    mask = cv2.bitwise_and(mask_l, mask_s)

    # Limpiar ruido
    kernel = np.ones((5,5), np.uint8)

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    # Filtrar componentes pequeñas
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
        mask,
        connectivity=8
    )

    final_mask = np.zeros_like(mask)

    for i in range(1, num_labels):

        area = stats[i, cv2.CC_STAT_AREA]

        if 80 < area < 50000:

            final_mask[labels == i] = 255

    # Crear overlay rojo suave
    # Expandir regiones detectadas
    kernel_expand = np.ones((25,25), np.uint8)

    expanded_mask = cv2.dilate(
        final_mask,
        kernel_expand,
        iterations=1
    )

    # Suavizar bordes
    blurred_mask = cv2.GaussianBlur(
        expanded_mask,
        (31,31),
        0
    )

    # Normalizar intensidad
    blurred_mask = blurred_mask.astype(np.float32) / 255.0

    # Crear overlay rojo
    overlay = img_rgb.copy().astype(np.float32)

    red_layer = np.zeros_like(overlay)

    red_layer[:,:,0] = 255

    # Intensidad variable
    alpha = blurred_mask * 0.45

    # Aplicar overlay suave
    for c in range(3):

        overlay[:,:,c] = (
            overlay[:,:,c] * (1 - alpha)
            + red_layer[:,:,c] * alpha
        )

    result = np.clip(
        overlay,
        0,
        255
    ).astype(np.uint8)

    return result




# -----------------------------
# CONVERTIR IMAGEN A BASE64
# -----------------------------
def image_to_base64(img_rgb):

    img_bgr = cv2.cvtColor(
        img_rgb,
        cv2.COLOR_RGB2BGR
    )

    _, buffer = cv2.imencode(".jpg", img_bgr)

    return base64.b64encode(buffer).decode("utf-8")


# -----------------------------
# GUARDAR IMAGEN TEMPORAL
# -----------------------------
def guardar_imagen_visual(img_rgb):

    temp_dir = "temp_visuals"

    os.makedirs(temp_dir, exist_ok=True)

    filename = f"{uuid.uuid4()}.jpg"

    filepath = os.path.join(temp_dir, filename)

    img_bgr = cv2.cvtColor(
        img_rgb,
        cv2.COLOR_RGB2BGR
    )

    cv2.imwrite(filepath, img_bgr)

    return filename



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

        # Generar visualización
        visual = detectar_vitiligo_visual(img_resized)

    else:

        diagnostico = "no_vitiligo"
        confianza = float(1 - pred)

        # Imagen normal
        visual = img_resized

    # Convertir visualización a base64
    filename_visual = guardar_imagen_visual(visual)
    
    imagen_url = f"/temp_visuals/{filename_visual}"
    return {
        "diagnostico": diagnostico,
        "confianza": confianza,
        "imagen_visual": imagen_url
    }