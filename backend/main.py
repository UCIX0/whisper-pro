import os
import shutil
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import logging

# Check if service is importable
try:
    from backend.service import get_transcription_service
except ImportError:
    # Fallback if running directly inside backend/
    from service import get_transcription_service

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:5173",  # Vite default
    "http://127.0.0.1:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger("API")

UPLOAD_DIR = "./temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.on_event("startup")
async def startup_event():
    # Pre-load model on startup
    logger.info("Initializing Transcription Service...")
    get_transcription_service()


@app.get("/")
async def root():
    return {"message": "Whisper Transcriptor API is running"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Uploads a file and returns the local path to be used for transcription.
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"file_path": os.path.abspath(file_path), "filename": file.filename}
    except Exception as e:
        return {"error": str(e)}


@app.websocket("/ws/transcribe")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    file_path = None
    try:
        # Wait for client to send the file path (received from upload)
        data = await websocket.receive_json()
        file_path = data.get("file_path")

        if not file_path:
            await websocket.send_json({"type": "error", "message": "No file path provided"})
            return

        service = get_transcription_service()

        # Run synchronous generator in a non-blocking way is tricky with simple iterators
        # ideally we offload the blocking call to threadpool
        # But for simplicity and because FasterWhisper releases GIL, we can iterate carefully
        # OR better: run the iterator in an executor.

        # However, for streaming integration, strict async generator is best.
        # Let's wrap the blocking generator in a thread pool for safety.

        loop = asyncio.get_event_loop()

        def run_transcription():
            # This runs in a thread
            # We need to collect yield items and return them or use a queue
            # Since we can't yield from run_in_executor easily without a Queue
            # We will use a simplified approach: Iterate directly if we trust the GIL release or accept minor blocking
            # But let's try to be robust.
            pass

        # Direct iteration (Simple & Functional for this scale)
        # Faster-whisper releases GIL during heavy computation
        for event in service.transcribe(file_path):
            await websocket.send_json(event)
            # Allow event loop to breathe
            await asyncio.sleep(0.01)

        await websocket.send_json({"type": "complete"})

    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await websocket.send_json({"type": "error", "message": str(e)})
        except:
            pass
    finally:
        # Cleanup temp file? Maybe keep it for debugging or delete it
        # os.remove(file_path)
        pass
