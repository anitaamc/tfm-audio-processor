import os
import speech_recognition as sr
from pydub import AudioSegment
from flask import jsonify


def transcribe_audio(audio_file):
    try:
        # Convertir el archivo de audio a formato PCM WAV
        if not audio_file.endswith('.wav'):
            wav_file = os.path.splitext(audio_file)[0] + '.wav'
            audio = AudioSegment.from_file(audio_file)
            audio.export(wav_file, format='wav', parameters=['-ac', '1', '-ar', '16000'])
        else:
            wav_file = audio_file

        # Transcribir el archivo de audio en formato PCM WAV
        r = sr.Recognizer()
        with sr.AudioFile(wav_file) as source:
            audio = r.record(source)
            transcript = r.recognize_google(audio, language='es-ES')
            print(transcript)

        # Eliminar el archivo de audio WAV temporal si se realizó la conversión
        if not audio_file.endswith('.wav'):
            os.remove(wav_file)

        return transcript

    except Exception as e:
        # Manejo de errores
        print(f"Error durante la transcripción del audio: {str(e)}")
        return None


def search_keyword(transcript):
    # Ejemplo de búsqueda de palabra clave en el texto transcribido
    keyword_found = False
    message = "Palabra clave no encontrada."

    if "pepito" in transcript.lower():
        keyword_found = True
        message = "Simulando activación del modo emergencia. Llamando a emergencias. Cerrando puertas y cajas fuertes. Tomando medidas preestablecidas para el estado de emergencia."

    return keyword_found, message


def process_audio(audio_file):
    try:
        # Verificar si el archivo de audio existe
        if not os.path.isfile(audio_file):
            return jsonify({'message': 'No hay grabación para procesar.'})

        # Transcribir el audio
        transcript = transcribe_audio(audio_file)

        if transcript is not None:
            # Buscar palabra clave en el texto transcribido
            keyword_found, message = search_keyword(transcript)

            if keyword_found:
                return jsonify({'message': message})

        return jsonify({'message': 'Palabra clave no encontrada.'})

    except Exception as e:
        # Manejo de errores
        print(f"Error durante el procesamiento del audio: {str(e)}")
        return jsonify({'message': 'Error en el procesamiento del audio.'})
