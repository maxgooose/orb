"""
ORB — Main Control Loop
Listen → Detect Emotion → Decide Response → Act

This is the core loop that ties everything together.
"""
import time
import signal
import logging
import sys

from .audio.listener import AudioListener
from .audio.features import extract_features
from .emotion.classifier import classify
from .brain.claude_brain import ClaudeBrain
from .hardware.motors import Motors
from .hardware.leds import LEDRing
from .hardware.speaker import Speaker
from .hardware.imu import IMU
from .utils.mood_history import MoodHistory
from .utils.config import get

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("orb")


class Orb:
    """The emotional companion ball."""

    def __init__(self):
        self.mood_history = MoodHistory(max_size=get("behavior.mood_history_size", 10))

        # Initialize all subsystems
        self.listener = AudioListener()
        self.brain = ClaudeBrain(self.mood_history)
        self.motors = Motors()
        self.leds = LEDRing()
        self.speaker = Speaker()
        self.imu = IMU()

        self._running = False

    def setup(self):
        """Initialize all hardware."""
        logger.info("🔮 ORB starting up...")
        self.motors.setup()
        self.leds.setup()
        self.speaker.setup()
        self.imu.setup()
        self.listener.start()

        # Startup animation: breathing white
        self.leds.breathe("#E8E8FF", duration=2.0, cycles=1)
        logger.info("🔮 ORB ready. Listening...")

    def run(self):
        """Main loop: listen → detect → decide → act."""
        self._running = True
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)

        self.setup()

        # Idle breathing color
        self.leds.set_color_hex("#E8E8FF")

        while self._running:
            try:
                self._tick()
            except Exception as e:
                logger.error(f"Loop error: {e}", exc_info=True)
                time.sleep(1)

        self.shutdown()

    def _tick(self):
        """One cycle of the main loop."""
        # Check if ball is being picked up → pause and wait
        if self.imu.is_picked_up():
            logger.info("🤚 Picked up — pausing")
            self.leds.breathe("#88CCFF", duration=2.0)
            time.sleep(2)
            return

        # Record audio window
        audio = self.listener.record_window()
        if audio is None:
            time.sleep(0.5)
            return

        # Check for prolonged silence (special case)
        if not self.listener.is_voice_active(audio) and self.listener.is_prolonged_silence:
            mood, confidence = "silent", 0.9
            logger.info(f"😶 Prolonged silence ({self.listener.silence_duration:.0f}s)")
        elif not self.listener.is_voice_active(audio):
            # Short silence — just idle
            self.leds.execute_glow("#E8E8FF", 0.3)  # Gentle idle glow
            return
        else:
            # Extract features and classify
            features = extract_features(audio)
            mood, confidence = classify(features)
            logger.info(f"🎭 Detected: {mood} ({confidence:.0%})")

        # Ask the brain what to do
        action = self.brain.decide(mood, confidence)
        logger.info(
            f"🧠 Action: move={action.movement}, color={action.color}, "
            f"msg='{action.message}', intensity={action.intensity:.0%}"
        )

        # Execute the response
        self._execute(action)

        # Cool-down between cycles
        time.sleep(1.0)

    def _execute(self, action):
        """Execute a physical response."""
        # LED glow (non-blocking visual)
        self.leds.execute_glow(action.color, action.intensity)

        # Movement
        self.motors.execute_movement(action.movement, action.intensity)

        # Speak (if there's a message)
        if action.message:
            self.speaker.speak(action.message)

    def shutdown(self):
        """Clean shutdown."""
        logger.info("🔮 ORB shutting down...")
        self._running = False
        self.leds.breathe("#FF6B6B", duration=1.0)  # Goodbye pulse
        self.leds.off()
        self.listener.stop()
        self.motors.cleanup()
        self.speaker.cleanup()
        self.imu.cleanup()
        logger.info("🔮 Goodbye.")

    def _handle_shutdown(self, signum, frame):
        self._running = False


def main():
    orb = Orb()
    orb.run()


if __name__ == "__main__":
    main()
