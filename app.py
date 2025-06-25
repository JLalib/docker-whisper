import subprocess
import os
import zipfile
import schedule
import time
import threading
from flask import Flask, render_template, request, send_file, after_this_request
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No se encontró el archivo en la solicitud", 400
    file = request.files['file']
    
    if file.filename == '':
        return "No se seleccionó ningún archivo", 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    language = request.form.get('language')
    if not language:
        return "Idioma no especificado", 400

    try:
        transcribed_file = transcribe_video(file_path, language)
        compressed_file = compress_file(transcribed_file)
    except Exception as e:
        return f"Error durante el procesamiento: {str(e)}", 500

    @after_this_request
    def remove_files(response):
        clean_up(file_path, transcribed_file, compressed_file)
        return response

    return send_file(
        compressed_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name=os.path.basename(compressed_file)
    )

def transcribe_video(file_path, language):
    absolute_file_path = os.path.abspath(file_path)

    command = [
        'whisper', absolute_file_path,
        '--model', 'base', 
        '--language', language, 
        '--output_format', 'txt', 
        '--output_dir', RESULTS_FOLDER
    ]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise Exception(f"Error al transcribir el vídeo: {stderr.decode()}")

    filename = f"{os.path.splitext(os.path.basename(file_path))[0]}.txt"
    transcribed_file = os.path.join(RESULTS_FOLDER, filename)

    if os.path.exists(transcribed_file):
        return transcribed_file
    else:
        raise Exception("El archivo de transcripción no se generó correctamente.")

def compress_file(file_path):
    if not os.path.exists(file_path):
        raise Exception(f"El archivo {file_path} no existe, no se puede comprimir.")

    zip_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}.zip"
    zip_filepath = os.path.join(RESULTS_FOLDER, zip_filename)

    with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_path, os.path.basename(file_path))

    return zip_filepath

def clean_up(uploaded_file, transcribed_file, zip_file):
    try:
        os.remove(uploaded_file)
        os.remove(transcribed_file)
        os.remove(zip_file)
    except Exception as e:
        print(f"Error al limpiar los archivos: {str(e)}")

# ---- Programación de limpieza diaria ----
def limpiar_archivos_programado():
    for folder in [UPLOAD_FOLDER, RESULTS_FOLDER]:
        for f in os.listdir(folder):
            file_path = os.path.join(folder, f)
            try:
                os.remove(file_path)
                print(f"Archivo eliminado: {file_path}")
            except Exception as e:
                print(f"Error al borrar {file_path}: {e}")

def run_scheduler():
    schedule.every().day.at("00:00").do(limpiar_archivos_programado)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=run_scheduler, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, debug=True)
