from flask import Flask, render_template, request, jsonify
import os
from audio_processing import process_audio

app = Flask(__name__)

keywords = ['pepito']

# Variable para almacenar el audio grabado
recorded_audio = None

# Ruta principal para cargar la interfaz web
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para sobrescribir las palabras clave
@app.route('/overwrite_keywords', methods=['POST'])
def overwrite_keywords():
    global keywords
    new_keywords = request.json.get('keywords', [])
    if new_keywords:
        keywords = new_keywords
        return jsonify({'message': 'Palabras clave sobreescritas correctamente'})
    else:
        return jsonify({'message': 'Error al sobrescribir las palabras clave'})


# Ruta para iniciar la grabación de audio
@app.route('/start_recording', methods=['POST'])
def start_recording():
    global recorded_audio
    recorded_audio = None
    return jsonify({'message': 'Grabando...'})

@app.route('/save_audio', methods=['POST'])
def save_audio():
    global recorded_audio
    audio_file = 'audio.wav'
    if os.path.exists(audio_file):
        os.remove(audio_file)
    audio_data = request.files['audio']
    audio_data.save(audio_file)
    return process_audio(audio_file)


if __name__ == '__main__':
    app.run(debug=True)
