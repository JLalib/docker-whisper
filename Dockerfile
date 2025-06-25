# Usa una imagen oficial de Python
FROM python:3.10-slim

# Instala ffmpeg (requerido por Whisper)
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto del servidor Flask
EXPOSE 5000

# Comando para iniciar la aplicación
CMD ["python", "app.py"]

