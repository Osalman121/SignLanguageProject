import asyncio
import websockets
import pyaudio
import json

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 4000

async def send_audio_stream(ws, stream):
    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            await ws.send(data)
            await asyncio.sleep(0.001)
    except Exception as e:
        print(f"Microphone error: {e}")

async def receive_transcription(ws):
    try:
        while True:
            message = await ws.recv()
            result = json.loads(message)
            if result.get("type") == "final":
                print(f"\n[FINAL]: {result['text']}\n")
            elif result.get("type") == "partial":
                print(f"[partial]: {result['text']}", end='\r')
    except websockets.exceptions.ConnectionClosed:
        pass

async def main():
    uri = "ws://127.0.0.1:8000/api/en/ws/stt"
    print(f"Connecting to WebSocket server at {uri}...")
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    try:
        async with websockets.connect(uri) as ws:
            print("Connected! Start speaking into your microphone...")
            await asyncio.gather(send_audio_stream(ws, stream), receive_transcription(ws))
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    asyncio.run(main())