import sounddevice as sd
import numpy as np
import wave
import time
import os
import requests
import warnings
import speech_recognition as sr
from config import DEEPGRAM_API_KEY

warnings.simplefilter('ignore')

# ========================== CONFIG ==========================
SILENCE_LIMIT = 2.0            # Seconds of silence before stopping
SAMPLE_RATE = 16000
CHUNK_DURATION = 0.3           # Seconds per audio chunk
CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_DURATION)
AUDIO_FILENAME = "temp_audio.wav"
ambient_rms = None 
device_index=1            # will be updated after calibration
# ============================================================


def calibrate_noise(duration=1.0):
    """Calibrate background noise using 1 second of silence."""
    global ambient_rms
    print("🤫 Calibrating ambient noise... please stay silent.")
    noise = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16',device=device_index)
    sd.wait()
    noise = noise.flatten().astype(np.float32) / 32768.0  # Normalize to [-1, 1]
    ambient_rms = np.sqrt(np.mean(np.square(noise)))
    print(f"📉 Calibrated ambient RMS: {ambient_rms:.6f}")
    return ambient_rms


def is_speech(chunk, threshold=None):
    """Detect if current chunk contains speech."""
    global ambient_rms
    chunk = chunk.astype(np.float32) / 32768.0  
    rms = np.sqrt(np.mean(np.square(chunk)))
    if threshold is None:
        threshold = ambient_rms * 1.8 if ambient_rms else 0.02
    # print(f"🔊 Chunk RMS: {rms:.6f}, Threshold: {threshold:.6f}")
    print(threshold,rms)
    return rms > threshold


def record_until_silence(filename=AUDIO_FILENAME):
    """Record user's voice and auto-stop when silence detected."""
    print("🎙️ Start speaking... (auto-stops on silence)")
    recording = []
    silent_chunks = 0

    with sd.InputStream(device=device_index,samplerate=SAMPLE_RATE, channels=1, dtype='int16') as stream:
        while True:
            chunk, _ = stream.read(CHUNK_SIZE)
            chunk = chunk.flatten()
            recording.append(chunk)

            if is_speech(chunk):
                silent_chunks = 0
            else:
                silent_chunks += 1

            # print(f"🟨 Silent for: {silent_chunks * CHUNK_DURATION:.1f}s")
            print(silent_chunks)

            if silent_chunks * CHUNK_DURATION > SILENCE_LIMIT:
                break

    audio_data = np.concatenate(recording)
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit PCM
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_data.tobytes())

    print("✅ Recording stopped and saved.")
    return filename


def transcribe_with_deepgram(audio_path):
    try:
        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": "audio/wav"
        }
        with open(audio_path, 'rb') as audio:
            response = requests.post("https://api.deepgram.com/v1/listen", headers=headers, data=audio)
        result = response.json()
        return result["results"]["channels"][0]["alternatives"][0]["transcript"]
    except Exception as e:
        print(f"❌ Deepgram failed: {e}")
        return ""


def transcribe_with_google(audio_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = recognizer.record(source)
        return recognizer.recognize_google(audio_data)
    except Exception as e:
        print(f"⚠️ Google STT failed: {e}")
        return ""


def listen():
    audio_file = record_until_silence()
    if not audio_file or not os.path.exists(audio_file):
        return ""

    if os.path.getsize(audio_file) < 1000:
        print("⚠️ Audio file is too small or silent.")
        os.remove(audio_file)
        return ""

    text = transcribe_with_deepgram(audio_file)

    if not text:
        print("🌀 Falling back to Google speech recognition...")
        text = transcribe_with_google(audio_file)

    if os.path.exists(audio_file):
        os.remove(audio_file)

    return text.lower().strip() if text else ""
