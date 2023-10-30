from .engine import AudioEngine
# from app.audio.engine import AudioEngine

def create_audio_engine(input_wav):
    return AudioEngine(input_wav)
