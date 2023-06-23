import os
import speech_recognition as sr
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

def detect_keyword(audio_path, keyword):
    r = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)  # Leer el archivo de audio

    try:
        text = r.recognize_google(audio, language='es-ES')  # Reconocer el texto del audio
        if keyword in text:
            return True
    except sr.UnknownValueError:
        pass

    return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    keyword = request.form['keyword']
    audio_file = request.files['audio']
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'audio.wav')
    audio_file.save(audio_path)

    result = detect_keyword(audio_path, keyword)

    if result:
        message = "Simulando activación del modo emergencia. Llamando a emergencias. Cerrando puertas y cajas fuertes. Tomando medidas preestablecidas para el estado de emergencia."
    else:
        message = "No se detectaron las palabras clave."

    os.remove(audio_path)  # Eliminar el archivo de audio después de su procesamiento

    return render_template('result.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
