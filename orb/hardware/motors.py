"""
L298N motor driver control for pendulum-drive ball.
Two DC motors create differential steering inside the globe.
"""
import time
import logging
from ..utils.config import get

logger = logging.getLogger("orb.hardware")

try:
    import RPi.GPIO as GPIO
    HAS_GPIO = True
except ImportError:
    HAS_GPIO = False
    logger.info("RPi.GPIO not available — motor control in simulation mode")


class Motors:
    def __init__(self):
        self.pins = {
            "lf": get("motors.left_forward", 17),
            "lb": get("motors.left_backward", 27),
            "rf": get("motors.right_forward", 22),
            "rb": get("motors.right_backward", 23),
            "el": get("motors.enable_left", 12),
            "er": get("motors.enable_right", 13),
        }
        self.speed = get("motors.speed", 60)
        self._pwm_left = None
        self._pwm_right = None
        self._initialized = False

    def setup(self):
        if not HAS_GPIO:
            logger.info("Motors: simulation mode")
            self._initialized = True
            return

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        for pin in self.pins.values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

        self._pwm_left = GPIO.PWM(self.pins["el"], 1000)
        self._pwm_right = GPIO.PWM(self.pins["er"], 1000)
        self._pwm_left.start(0)
        self._pwm_right.start(0)
        self._initialized = True
        logger.info("Motors initialized")

    def _set_speed(self, speed: int):
        if self._pwm_left:
            self._pwm_left.ChangeDutyCycle(speed)
        if self._pwm_right:
            self._pwm_right.ChangeDutyCycle(speed)

    def forward(self, duration: float = 1.0, speed: int = None):
        """Roll forward (toward user)."""
        speed = speed or self.speed
        logger.debug(f"Forward {duration}s at {speed}%")
        if not HAS_GPIO:
            time.sleep(duration)
            return
        self._set_motors(True, False, True, False, speed)
        time.sleep(duration)
        self.stop()

    def backward(self, duration: float = 1.0, speed: int = None):
        """Roll backward (away from user)."""
        speed = speed or self.speed
        logger.debug(f"Backward {duration}s at {speed}%")
        if not HAS_GPIO:
            time.sleep(duration)
            return
        self._set_motors(False, True, False, True, speed)
        time.sleep(duration)
        self.stop()

    def spin(self, duration: float = 1.0, speed: int = None):
        """Spin in place (celebration)."""
        speed = speed or self.speed
        logger.debug(f"Spin {duration}s at {speed}%")
        if not HAS_GPIO:
            time.sleep(duration)
            return
        self._set_motors(True, False, False, True, speed)
        time.sleep(duration)
        self.stop()

    def nudge(self, duration: float = 0.5):
        """Quick forward nudge."""
        self.forward(duration, speed=40)

    def stop(self):
        """Stop all motors."""
        if not HAS_GPIO:
            return
        for pin_name in ["lf", "lb", "rf", "rb"]:
            GPIO.output(self.pins[pin_name], GPIO.LOW)
        self._set_speed(0)

    def _set_motors(self, lf: bool, lb: bool, rf: bool, rb: bool, speed: int):
        if not HAS_GPIO:
            return
        GPIO.output(self.pins["lf"], GPIO.HIGH if lf else GPIO.LOW)
        GPIO.output(self.pins["lb"], GPIO.HIGH if lb else GPIO.LOW)
        GPIO.output(self.pins["rf"], GPIO.HIGH if rf else GPIO.LOW)
        GPIO.output(self.pins["rb"], GPIO.HIGH if rb else GPIO.LOW)
        self._set_speed(speed)

    def execute_movement(self, movement: str, intensity: float = 0.5):
        """Execute a movement command from the AI brain."""
        speed = int(self.speed * intensity)
        duration = get("behavior.approach_distance_sec", 3) * intensity

        if movement == "toward":
            self.forward(duration, speed)
        elif movement == "away":
            self.backward(duration * 0.5, speed)
        elif movement == "circle":
            spins = get("behavior.celebration_spins", 2)
            for _ in range(spins):
                self.spin(0.8, speed)
                time.sleep(0.2)
        elif movement == "nudge":
            self.nudge(get("behavior.nudge_duration_sec", 0.5))
        elif movement == "still":
            pass  # Do nothing

    def cleanup(self):
        if HAS_GPIO:
            self.stop()
            GPIO.cleanup()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    m = Motors()
    m.setup()
    print("Testing motors (simulation mode if no GPIO)...")
    m.forward(1)
    m.spin(1)
    m.nudge()
    m.backward(0.5)
    m.cleanup()
    print("Done.")
