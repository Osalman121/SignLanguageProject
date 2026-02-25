from vosk import Model, KaldiRecognizer
from app.core.config import VOSK_MODEL_EN_PATH, VOSK_MODEL_AR_PATH

class VoskService:
    def __init__(self):
        print("Loading Vosk Models into memory... This might take a few seconds.")
        # Load models ONCE into RAM
        self.model_en = Model(VOSK_MODEL_EN_PATH)
        self.model_ar = Model(VOSK_MODEL_AR_PATH)
        print("Vosk Models loaded successfully!")

    def create_recognizer(self, language: str = "en", sample_rate: int = 16000) -> KaldiRecognizer:
        """
        Creates a fresh recognizer instance for a new WebSocket session.
        """
        model = self.model_ar if language == "ar" else self.model_en
        return KaldiRecognizer(model, sample_rate)

# THIS is the missing variable the error is complaining about!
vosk_engine = VoskService()