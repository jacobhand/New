import pyaudio
import wave
import os
from pydub import AudioSegment

def record_audio_to_mp3(mp3_filename, record_seconds):
    # Einstellungen
    FORMAT = pyaudio.paInt16
    CHANNELS = 1  # Setze die Anzahl der Kanäle auf 1
    RATE = 44100
    CHUNK = 1024
    WAVE_OUTPUT_FILENAME = "temp_output.wav"

    audio = pyaudio.PyAudio()

    # Start Aufnahme
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Aufnahme gestartet...")

    frames = []

    for i in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Aufnahme beendet.")

    # Stop Aufnahme
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Speichern in eine WAV-Datei
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    # Konvertiere WAV zu MP3 und lösche die WAV-Datei
    audio_segment = AudioSegment.from_wav(WAVE_OUTPUT_FILENAME)
    audio_segment.export(mp3_filename, format="mp3")
    os.remove(WAVE_OUTPUT_FILENAME)

    print(f"Datei gespeichert als {mp3_filename}")

