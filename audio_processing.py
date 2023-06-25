import speech_recognition as sr
from flask import jsonify

def transcribe_audio(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
        transcript = r.recognize_google(audio, language='es-ES')
        print(transcript)
    return transcript

def process_audio(audio_file):
    # Verificar si el archivo de audio existe
    import os
    if not os.path.isfile(audio_file):
        return jsonify({'message': 'No hay grabación para procesar.'})

    # Aquí se realiza el procesamiento y búsqueda de la palabra clave en el archivo de audio

    # Ejemplo de búsqueda de palabra clave en el texto transcribido, esto se refactorizaría y se implementaría para un caso de uso real en una segunda iteración, esto es solo una prueba de concepto
    keyword_found = False
    message = "Palabra clave no encontrada."
    transcript = transcribe_audio(audio_file)
    if "pepito" in transcript.lower():
        keyword_found = True
        message = "Simulando activación del modo emergencia. Llamando a emergencias. Cerrando puertas y cajas fuertes. Tomando medidas preestablecidas para el estado de emergencia."

    return jsonify({'message': message})
