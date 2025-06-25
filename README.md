# 🎙️ Whisper Transcriptor Web

Aplicación web basada en Flask para transcribir vídeos automáticamente usando el modelo Whisper de OpenAI.

## 🚀 Características

- Subida de vídeos `.mp4`, `.avi` o `.mkv`
- Transcripción automática en **Español**, **Inglés** o **Portugués**
- Descarga del resultado en `.zip`
- Limpieza automática de archivos cada medianoche
- Interfaz web ligera, funcional y sin dependencias externas

---

## 📁 Estructura del proyecto

```
whisper/
├── app.py                 # Backend Flask
├── Dockerfile             # Imagen Docker
├── docker-compose.yml     # (opcional) Orquestación si se usa
├── requirements.txt       # Dependencias Python
├── templates/
│   └── index.html         # Interfaz web (Jinja2)
├── static/
│   ├── style.css
│   ├── script.js
│   └── favicon.png
├── uploads/               # Archivos de vídeo temporales
├── results/               # Archivos de texto y .zip generados
```

---

## ⚙️ Requisitos

- Python 3.10+
- `ffmpeg` instalado en el sistema
- Docker (opcional, recomendado)
- Requiere acceso a internet para descargar modelos Whisper la primera vez

---

## 🧪 Instalación local

```bash
pip install -r requirements.txt
python app.py
```

Accede a: [http://localhost:5000](http://localhost:5000)

---

## 🐳 Uso con Docker

### 1. Construir la imagen

```bash
docker build -t whisper-app .
```

### 2. Ejecutar el contenedor

```bash
docker run -p 5000:5000 whisper-app
```

---

## 🧼 Limpieza automática

La app elimina diariamente a las 00:00 todos los archivos temporales en `uploads/` y `results/` usando un programador (`schedule` + `threading`).

---

## 🧠 Créditos

- Basado en [Whisper](https://github.com/openai/whisper)
- Proyecto personalizado por Javier Cascallana



