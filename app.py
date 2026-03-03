import os
import sys
import numpy as np
import sounddevice as sd
import soundfile as sf

# -----------------------------
# FFmpeg Setup (Windows-safe)
# -----------------------------
ffmpeg_path = r"C:\ffmpeg-8.0.1-full_build\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe"  # <- update this if your ffmpeg.exe is elsewhere
if not os.path.isfile(ffmpeg_path):
    raise FileNotFoundError(f"FFmpeg executable not found at {ffmpeg_path}")
os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path
os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)

# -----------------------------
# Import internal modules
# -----------------------------
from src.asr_engine import ASREngine

# -----------------------------
# Ensure folders exist
# -----------------------------
os.makedirs("data/samples", exist_ok=True)

# -----------------------------
# Audio Recording Utility
# -----------------------------
def record_audio(duration=30, output_path="data/samples/live_recording.wav", samplerate=16000):
    """
    Record audio from the microphone and save as WAV.
    duration: seconds
    """
    print(f"Recording for {duration} seconds... Speak now.")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()
    sf.write(output_path, audio, samplerate)
    print(f"Audio saved at {output_path}")
    return output_path

# -----------------------------
# Optional: Validate audio
# -----------------------------
def validate_audio(path):
    if not os.path.isfile(path):
        print("File does not exist.")
        return False
    if not path.lower().endswith(".wav"):
        print("File is not a WAV file.")
        return False
    return True

# -----------------------------
# Main ASR Application
# -----------------------------
def main():
    print("Starting ASR Application...")
    
    engine = ASREngine()
    
    # Ask user: record or use existing file
    choice = input("Record (r) or Use existing file (f)? ").strip().lower()
    
    if choice == "r":
        # You can change duration here if you want
        duration = input("Enter recording length in seconds (default 30): ").strip()
        duration = int(duration) if duration.isdigit() else 30
        audio_path = record_audio(duration=duration)
    else:
        audio_path = input("Enter audio file path: ").strip()
    
    if not validate_audio(audio_path):
        print("Invalid audio. Exiting.")
        return
    
    print("\nTranscribing in both English and Urdu... Please wait.")
    
    # Transcribe in English
    result_en = engine.transcribe(audio_path, language="en")
    
    # Transcribe in Urdu
    result_ur = engine.transcribe(audio_path, language="ur")
    
    print("\n--- Transcription Result ---")
    print("English Transcription:", result_en["text"])
    print("Urdu Transcription:", result_ur["text"])

# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    main()