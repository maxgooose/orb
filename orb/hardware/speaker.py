"""
Text-to-speech output for ORB comfort messages.
Supports pyttsx3 (offline) with optional ElevenLabs upgrade.
"""
import logging
from ..utils.config import get

logger = logging.getLogger("orb.hardware")

try:
    import pyttsx3
    HAS_PYTTSX3 = True
except ImportError:
    HAS_PYTTSX3 = False


class Speaker:
    def __init__(self):
        self.engine_type = get("speaker.engine", "pyttsx3")
        self.volume = get("speaker.volume", 0.7)
        self._engine = None

    def setup(self):
        if HAS_PYTTSX3:
            try:
                self._engine = pyttsx3.init()
                self._engine.setProperty("volume", self.volume)
                self._engine.setProperty("rate", 140)  # Slower, warmer
                logger.info("Speaker initialized (pyttsx3)")
            except Exception as e:
                logger.warning(f"pyttsx3 init failed: {e}")
        else:
            logger.info("Speaker: simulation mode (no TTS engine)")

    def speak(self, message: str):
        """Speak a short comfort message."""
        if not message:
            return

        logger.info(f"Speaking: '{message}'")

        if self._engine:
            try:
                self._engine.say(message)
                self._engine.runAndWait()
            except Exception as e:
                logger.error(f"Speech error: {e}")
        else:
            logger.debug(f"[SIM] Would say: '{message}'")

    def cleanup(self):
        if self._engine:
            try:
                self._engine.stop()
            except Exception:
                pass
