"""
FRIDAY AI Operating System
Production Microphone Service

This service owns the microphone for the entire application.

Responsibilities
----------------
• Detect microphone
• Open audio stream
• Capture audio continuously
• Push AudioFrame objects into a thread-safe queue
• Handle recovery from device failures
• Graceful shutdown

This module NEVER performs:
• Wake word detection
• Speech recognition
• AI processing
• Audio playback
"""

from __future__ import annotations

import queue
import threading
import time
from datetime import datetime
from typing import Optional

import numpy as np
import sounddevice as sd

from .audio_stream import AudioFrame
from .exceptions import (
    MicrophoneInitializationError,
)

DEFAULT_SAMPLE_RATE = 16000
DEFAULT_CHANNELS = 1
DEFAULT_BLOCK_DURATION_MS = 80


class MicrophoneService:
    """
    Production microphone service.

    This class owns the microphone for the lifetime
    of FRIDAY.

    Audio is published into a Queue<AudioFrame>.
    """

    def __init__(
        self,
        sample_rate: int = DEFAULT_SAMPLE_RATE,
        channels: int = DEFAULT_CHANNELS,
        block_duration_ms: int = DEFAULT_BLOCK_DURATION_MS,
        max_queue_size: int = 128,
        device: Optional[int] = None,
    ):

        self.sample_rate = sample_rate
        self.channels = channels
        self.block_duration_ms = block_duration_ms

        self.block_size = int(
            sample_rate * block_duration_ms / 1000
        )

        self.device = device

        self.audio_queue: queue.Queue[AudioFrame] = queue.Queue(
            maxsize=max_queue_size
        )

        self._stream: Optional[sd.InputStream] = None

        self._running = False
        self._paused = False

        self._frame_counter = 0

        self._lock = threading.RLock()

        self._worker_thread: Optional[threading.Thread] = None

        self._startup_time: Optional[datetime] = None
        self._last_frame_time: Optional[datetime] = None

        self._dropped_frames = 0

    @property
    def running(self) -> bool:
        return self._running

    @property
    def paused(self) -> bool:
        return self._paused

    @property
    def queue_size(self) -> int:
        return self.audio_queue.qsize()

    @property
    def dropped_frames(self) -> int:
        return self._dropped_frames

    def initialize(self) -> None:

        try:

            if self.device is None:
                self.device = sd.default.device[0]

            device_info = sd.query_devices(
                self.device,
                "input",
            )

            print("=" * 60)
            print("FRIDAY MICROPHONE")
            print("=" * 60)
            print("Device :", device_info["name"])
            print("Sample Rate :", self.sample_rate)
            print("Channels :", self.channels)
            print("Block Size :", self.block_size)
            print("=" * 60)

        except Exception as exc:
            raise MicrophoneInitializationError(
                str(exc)
            ) from exc

    def _audio_callback(
        self,
        indata,
        frames,
        time_info,
        status,
    ) -> None:
        """
        SoundDevice callback.
        """

        if status:
            print(status)

        if self._paused:
            return

        samples = np.copy(
            indata[:, 0]
        ).astype(np.float32)

        frame = AudioFrame(
            samples=samples,
            sample_rate=self.sample_rate,
            channels=self.channels,
            frame_index=self._frame_counter,
            timestamp=datetime.utcnow(),
        )

        self._frame_counter += 1
        self._last_frame_time = datetime.utcnow()

        try:
            self.audio_queue.put_nowait(frame)

        except queue.Full:
            self._dropped_frames += 1
        print("Audio callback running")
    def start(self) -> None:
        """
        Starts the microphone service.
        """

        with self._lock:

            if self._running:
                return

            self.initialize()

            self._stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype=np.float32,
                blocksize=self.block_size,
                callback=self._audio_callback,
                device=self.device,
            )

            self._stream.start()

            self._running = True
            self._paused = False
            self._startup_time = datetime.utcnow()

            self._worker_thread = threading.Thread(
                target=self._health_monitor,
                daemon=True,
                name="FridayAudioMonitor",
            )

            self._worker_thread.start()

            print("✅ Microphone service started.")

    def stop(self) -> None:
        """
        Stops microphone service.
        """

        with self._lock:

            if not self._running:
                return

            self._running = False
            self._paused = False

            try:

                if self._stream is not None:
                    self._stream.stop()
                    self._stream.close()

            finally:

                self._stream = None

            print("🛑 Microphone service stopped.")

    def pause(self) -> None:
        """
        Pause audio capture.
        """

        self._paused = True

    def resume(self) -> None:
        """
        Resume audio capture.
        """

        self._paused = False

    def clear_queue(self) -> None:
        """
        Remove all pending audio frames.
        """

        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except queue.Empty:
                break

    def read(self, timeout: Optional[float] = None) -> AudioFrame:
        """
        Read next available AudioFrame.

        Raises queue.Empty if timeout expires.
        """

        return self.audio_queue.get(timeout=timeout)

    def has_audio(self) -> bool:
        """
        Returns True if audio is waiting.
        """

        return not self.audio_queue.empty()

    def stats(self) -> dict:

        return {

            "running": self._running,

            "paused": self._paused,

            "queue_size": self.audio_queue.qsize(),

            "frames_received": self._frame_counter,

            "frames_dropped": self._dropped_frames,

            "last_frame": self._last_frame_time,

            "uptime": (
                datetime.utcnow() - self._startup_time
            ).total_seconds()
            if self._startup_time
            else 0,
        }

    def _health_monitor(self):
        """
        Background monitoring thread.

        Future responsibilities:

        • Device reconnect
        • Latency monitoring
        • Queue overflow monitoring
        • CPU statistics
        """

        while self._running:

            time.sleep(5)

            if not self._running:
                break

            if self.audio_queue.qsize() > 100:

                print(
                    f"⚠ Queue size is high ({self.audio_queue.qsize()})"
                )

            if self._last_frame_time is None:
                continue

            elapsed = (
                datetime.utcnow()
                - self._last_frame_time
            ).total_seconds()

            if elapsed > 2:

                print(
                    "⚠ No microphone data received for",
                    elapsed,
                    "seconds",
                )
        

    
        microphone_service = MicrophoneService()

    