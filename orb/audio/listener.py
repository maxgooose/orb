"""
Microphone listener with voice activity detection (VAD).
Captures audio chunks and determines when someone is speaking.
"""
import numpy as np
import time
import logging
from typing import Optional, Callable
from ..utils.config import get

logger = logging.getLogger("orb.audio")

# Try to import PyAudio; allow graceful fallback for dev machines
try:
    import pyaudio
    HAS_PYAUDIO = True
except ImportError:
    HAS_PYAUDIO = False
    logger.warning("PyAudio not available — using mock audio for development")


class AudioListener:
    """Captures audio from I2S MEMS microphone and detects voice activity."""

    def __init__(self):
        self.sample_rate = get("audio.sample_rate", 16000)
        self.chunk_size = get("audio.chunk_size", 1024)
        self.silence_threshold = get("audio.silence_threshold", 500)
        self.silence_timeout = get("audio.silence_timeout_sec", 30)
        self.record_seconds = get("audio.record_seconds", 3)

        self._stream = None
        self._pa = None
        self._last_voice_time = time.time()
        self._is_listening = False

    def start(self):
        """Open the microphone stream."""
        if not HAS_PYAUDIO:
            logger.info("Mock audio mode — no real microphone")
            self._is_listening = True
            return

        self._pa = pyaudio.PyAudio()
        self._stream = self._pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
        )
        self._is_listening = True
        logger.info(f"Listening at {self.sample_rate}Hz, chunk={self.chunk_size}")

    def stop(self):
        """Close the microphone stream."""
        self._is_listening = False
        if self._stream:
            self._stream.stop_stream()
            self._stream.close()
        if self._pa:
            self._pa.terminate()

    def read_chunk(self) -> Optional[np.ndarray]:
        """Read a single chunk of audio data. Returns numpy array of int16 samples."""
        if not self._is_listening:
            return None
        if not HAS_PYAUDIO or not self._stream:
            # Return synthetic silence for dev
            return np.zeros(self.chunk_size, dtype=np.int16)

        try:
            data = self._stream.read(self.chunk_size, exception_on_overflow=False)
            return np.frombuffer(data, dtype=np.int16)
        except Exception as e:
            logger.error(f"Audio read error: {e}")
            return None

    def record_window(self) -> Optional[np.ndarray]:
        """Record a full analysis window (default 3 seconds). Returns concatenated audio."""
        if not self._is_listening:
            return None

        chunks_needed = int(self.sample_rate * self.record_seconds / self.chunk_size)
        frames = []

        for _ in range(chunks_needed):
            chunk = self.read_chunk()
            if chunk is not None:
                frames.append(chunk)

        if not frames:
            return None
        return np.concatenate(frames)

    def get_rms(self, audio: np.ndarray) -> float:
        """Calculate root-mean-square energy of audio."""
        return float(np.sqrt(np.mean(audio.astype(np.float64) ** 2)))

    def is_voice_active(self, audio: np.ndarray) -> bool:
        """Simple VAD: is the RMS energy above the silence threshold?"""
        rms = self.get_rms(audio)
        if rms > self.silence_threshold:
            self._last_voice_time = time.time()
            return True
        return False

    @property
    def silence_duration(self) -> float:
        """Seconds since last detected voice activity."""
        return time.time() - self._last_voice_time

    @property
    def is_prolonged_silence(self) -> bool:
        """Has it been quiet for longer than the silence timeout?"""
        return self.silence_duration > self.silence_timeout


if __name__ == "__main__":
    """Quick test: run this module directly to verify mic works."""
    logging.basicConfig(level=logging.INFO)
    listener = AudioListener()
    listener.start()
    print("Listening... speak to test VAD. Ctrl+C to stop.")
    try:
        while True:
            chunk = listener.read_chunk()
            if chunk is not None:
                rms = listener.get_rms(chunk)
                active = "🔊 VOICE" if listener.is_voice_active(chunk) else "🔇 silence"
                bar = "█" * min(int(rms / 100), 40)
                print(f"\r{active} RMS:{rms:6.0f} {bar:<40}", end="", flush=True)
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        listener.stop()
