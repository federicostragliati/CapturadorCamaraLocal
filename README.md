# CapturadorCamUSB

Este script toma imágenes desde una cámara USB y las envía periódicamente a una API FastAPI para su evaluación con YOLOv8.

## Configuración

1. Editar `cam_sender.py` y cambiar `ENDPOINT` por la IP del servidor donde está corriendo la API.

2. Instalar dependencias:

```bash
pip install -r requirements.txt
