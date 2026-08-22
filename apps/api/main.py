from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.api.routes import voice_commands 
from apps.api.core.audio.microphone import MicrophoneService
from apps.api.core.wakeword.detector import wakeword_detector
from apps.api.core.voice.recorder import speech_recorder
from apps.api.core.voice.whisper_service import whisper_service
from apps.api.core.voice.transcript_processor import transcript_processor
from apps.api.core.execution.execution_Engine import execution_engine
from apps.api.routes import files, tts
app = FastAPI(
    title="FRIDAY",
    description="Personal AI Operating System Backend",
    version="0.1.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(files.router)
app.include_router(voice_commands.router)
app.include_router(tts.router)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "FRIDAY API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

    from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):

   

    MicrophoneService.start()
    print("Starting FRIDAY Runtime...")

    wakeword_detector.start()

    speech_recorder.start()

    whisper_service.start()

    transcript_processor.start()

    execution_engine.start()

    print("FRIDAY READY")

    yield

    print("Stopping FRIDAY Runtime...")

    MicrophoneService.stop()

    wakeword_detector.stop()

    speech_recorder.stop()

app = FastAPI(
    title="FRIDAY",
    lifespan=lifespan,
)