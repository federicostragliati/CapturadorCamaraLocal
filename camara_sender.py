import cv2
import requests
import time
import os
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import threading

class CapturadorUSB:
    def __init__(self, intervalo=30, endpoint="http://181.16.119.228:8090/imagen"):
        self.intervalo = intervalo
        self.endpoint = endpoint
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        print(f"[Init] Configurado cada {intervalo}s a {endpoint}")

    def capturar_y_enviar(self):
        ret, frame = self.cap.read()
        if ret:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = f"captura_{timestamp}.jpg"
            cv2.imwrite(image_path, frame)

            with open(image_path, "rb") as f:
                files = {"file": (image_path, f, "image/jpeg")}
                response = requests.post(self.endpoint, files=files)

            print(f"[{timestamp}] Imagen enviada")
            print("Respuesta:", response.json())
            os.remove(image_path)
        else:
            print("⚠️ No se pudo capturar imagen")

    def iniciar_bucle(self):
        while True:
            self.capturar_y_enviar()
            time.sleep(self.intervalo)

    def generar_frames(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                continue
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    def liberar(self):
        self.cap.release()


# -------------------------------
# API con FastAPI para el streaming
# -------------------------------
app = FastAPI()
capturador = CapturadorUSB()

@app.get("/video")
def video():
    return StreamingResponse(capturador.generar_frames(), media_type="multipart/x-mixed-replace; boundary=frame")


# -------------------------------
# Hilo separado para capturas periódicas
# -------------------------------
if __name__ == "__main__":
    import uvicorn

    hilo_captura = threading.Thread(target=capturador.iniciar_bucle, daemon=True)
    hilo_captura.start()

    print("Iniciando servidor FastAPI con endpoint /video...")
    uvicorn.run("camara_sender:app", host="0.0.0.0", port=8000, reload=False)
