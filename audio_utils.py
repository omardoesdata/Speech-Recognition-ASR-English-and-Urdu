import sounddevice as sd
import soundfile as sf
import numpy as np
from .config import SAMPLE_RATE


def record_audio(duration: int, output_path: str):
    """
    Records audio from microphone and saves as WAV file.
    """

    print("Recording... Speak now.")
    
    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )
    
    sd.wait()

    sf.write(output_path, audio, SAMPLE_RATE)

    print(f"Audio saved at {output_path}")
    return output_path


def validate_audio(file_path: str):
    """
    Checks if file exists and loads it.
    """
    try:
        data, sr = sf.read(file_path)
        return True
    except Exception as e:
        print("Invalid audio file:", e)
        return False