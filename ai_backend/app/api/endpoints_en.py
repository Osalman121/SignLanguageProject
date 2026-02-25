from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.stt_vosk import vosk_engine
import json

# This is the "router" that main.py is looking for!
router = APIRouter()

@router.websocket("/ws/stt")
async def websocket_stt_en(websocket: WebSocket):
    await websocket.accept()
    print("Client connected to English STT stream.")
    
    # Generate a dedicated recognizer for this specific phone connection
    recognizer = vosk_engine.create_recognizer(language="en")
    
    try:
        while True:
            # 1. Receive raw audio chunk from mobile microphone
            audio_bytes = await websocket.receive_bytes()
            
            # 2. Feed it to Vosk
            if recognizer.AcceptWaveform(audio_bytes):
                # A full sentence/phrase was completed
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                if text:
                    await websocket.send_json({"type": "final", "text": text})
            else:
                # The user is still speaking (live transcription)
                partial = json.loads(recognizer.PartialResult())
                partial_text = partial.get("partial", "")
                if partial_text:
                    await websocket.send_json({"type": "partial", "text": partial_text})
                    
    except WebSocketDisconnect:
        print("Client disconnected from STT stream.")