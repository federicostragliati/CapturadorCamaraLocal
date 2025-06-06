import cv2
import requests
import time
import os
from datetime import datetime

# -------------------------------
# Configuración
# -------------------------------
CAPTURA_CADA_SEGUNDOS = 10  # Frecuencia (2 capturas por minuto)
ENDPOINT = "http://localhost:8000/imagen"  # Cambiar si el backend está en otra IP

# -------------------------------
# Función principal
# -------------------------------
def capturar_y_enviar():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if ret:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = f"captura_{timestamp}.jpg"
        cv2.imwrite(image_path, frame)

        with open(image_path, "rb") as f:
            files = {"file": (image_path, f, "image/jpeg")}
            response = requests.post(ENDPOINT, files=files)

        print(f"[{timestamp}] Imagen enviada: {image_path}")
        print("Respuesta del servidor:", response.json())

        os.remove(image_path)
        print(f"Imagen eliminada: {image_path}")

    else:
        print("⚠️ Error: no se pudo capturar imagen.")

# -------------------------------
# Bucle principal
# -------------------------------
if __name__ == "__main__":
    print(f"Iniciando capturas cada {CAPTURA_CADA_SEGUNDOS} segundos...")
    while True:
        capturar_y_enviar()
        time.sleep(CAPTURA_CADA_SEGUNDOS)
