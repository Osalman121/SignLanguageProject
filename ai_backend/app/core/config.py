import os
from pathlib import Path

# Get the absolute path to the project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Define model paths (These match the folders you put in models/vosk_models/)
VOSK_MODEL_EN_PATH = os.path.join(BASE_DIR, "models", "vosk_models", "vosk-model-small-en-us-0.15") 
VOSK_MODEL_AR_PATH = os.path.join(BASE_DIR, "models", "vosk_models", "vosk-model-ar-mgb2-0.4")