import os
import time
import subprocess
import json
import logging
from faster_whisper import WhisperModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TranscriptionService")


class TranscriptionService:
    def __init__(self, model_path: str = "../modelo_whisper", device: str = "cuda", compute_type: str = "float16"):
        self.model_path = model_path
        self.device = device
        self.compute_type = compute_type
        self.model = None
        self._load_model()

    def _load_model(self):
        """Loads the Whisper model from the local path."""
        try:
            logger.info(
                f"Loading model from {self.model_path} on {self.device}...")
            start_load = time.time()

            # Ensure the path is absolute or correct relative to execution context
            # Assuming backend is run from /home/ucix/Música/Whisper/
            # Auto-download logic via download_root
            # We specify the model size 'large-v3' explicitly as the model_name
            # and use model_path as the download_root (storage location)
            self.model = WhisperModel(
                "large-v3",
                device=self.device,
                compute_type=self.compute_type,
                download_root=self.model_path
            )

            load_time = time.time() - start_load
            logger.info(
                f"Model loaded successfully in {load_time:.2f} seconds.")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise RuntimeError(f"Failed to load Whisper model: {e}")

    def get_audio_duration(self, file_path: str) -> float:
        """Gets audio duration using ffprobe."""
        try:
            cmd = [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                file_path
            ]
            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            data = json.loads(result.stdout)
            duration = float(data['format']['duration'])
            return duration
        except Exception as e:
            logger.error(f"Error getting duration for {file_path}: {e}")
            return 0.0

    def transcribe(self, file_path: str):
        """
        Generator that yields progress updates and transcribed text segments.
        Yields dicts: {"type": "progress" | "segment" | "info", "data": ...}
        """
        if not self.model:
            yield {"type": "error", "message": "Model not loaded."}
            return

        if not os.path.exists(file_path):
            yield {"type": "error", "message": f"File not found: {file_path}"}
            return

        try:
            duration = self.get_audio_duration(file_path)

            segments, info = self.model.transcribe(
                file_path,
                beam_size=5,
                language="es",
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=500)
            )

            yield {
                "type": "info",
                "data": {
                    "language": info.language,
                    "probability": info.language_probability,
                    "duration": duration
                }
            }

            for segment in segments:
                progress = 0
                if duration > 0:
                    progress = min(100, (segment.end / duration) * 100)

                yield {
                    "type": "segment",
                    "data": {
                        "start": segment.start,
                        "end": segment.end,
                        "text": segment.text,
                        "progress": progress
                    }
                }

        except Exception as e:
            logger.error(f"Transcription error: {e}")
            yield {"type": "error", "message": str(e)}


# Singleton instance to be cleaned up or managed by the app
# In a real generic app we might want dependency injection, but for this specific scope a global is fine.
service_instance = None


def get_transcription_service():
    global service_instance
    if service_instance is None:
        # Assuming run from root dir
        service_instance = TranscriptionService()
    return service_instance
