import whisper
import torch
from .config import MODEL_SIZE, DEVICE


class ASREngine:
    def __init__(self):
        print("Loading Whisper model...")
        self.device = DEVICE if torch.cuda.is_available() else "cpu"
        self.model = whisper.load_model(MODEL_SIZE).to(self.device)
        print(f"Model loaded on {self.device}")

    def transcribe(self, audio_path: str, language: str = None):
        """
        Transcribes given audio file.
        """

        result = self.model.transcribe(
            audio_path,
            language=language,
            fp16=(self.device == "cuda")
        )

        return {
            "language_detected": result["language"],
            "text": result["text"]
        }