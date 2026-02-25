from fastapi import FastAPI
from app.api import endpoints_en 

app = FastAPI(title="Sign Language Translation API")

# Mount the English WebSocket router
app.include_router(endpoints_en.router, prefix="/api/en", tags=["English"])

@app.get("/")
def health_check():
    return {"status": "Vosk STT Backend is live!"}