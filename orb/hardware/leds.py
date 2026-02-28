"""
NeoPixel LED ring control for mood-based lighting.
"""
import time
import math
import logging
from ..utils.config import get

logger = logging.getLogger("orb.hardware")

try:
    from rpi_ws281x import PixelStrip, Color
    HAS_NEOPIXEL = True
except ImportError:
    HAS_NEOPIXEL = False


# Mood color palettes
MOOD_COLORS = {
    "sad":      "#FFB347",  # Warm amber
    "happy":    "#00FF88",  # Bright green
    "stressed": "#4A90D9",  # Calm blue
    "silent":   "#FFFFFF",  # Soft white
    "neutral":  "#E8E8FF",  # Lavender white
}


def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to (R, G, B)."""
    hex_color = hex_color.lstrip("#")
    # Named colors
    named = {
        "amber": "FFB347", "blue": "4A90D9", "white": "FFFFFF",
        "rainbow": "FF0000", "red": "FF0000", "green": "00FF88",
    }
    if hex_color.lower() in named:
        hex_color = named[hex_color.lower()]
    if len(hex_color) != 6:
        hex_color = "FFFFFF"
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


class LEDRing:
    def __init__(self):
        self.count = get("leds.count", 16)
        self.pin = get("leds.pin", 18)
        self.brightness = get("leds.brightness", 0.5)
        self._strip = None

    def setup(self):
        if not HAS_NEOPIXEL:
            logger.info("LEDs: simulation mode")
            return
        self._strip = PixelStrip(self.count, self.pin, 800000, 10, False,
                                  int(self.brightness * 255), 0)
        self._strip.begin()
        logger.info(f"LED ring initialized: {self.count} LEDs on pin {self.pin}")

    def set_all(self, r: int, g: int, b: int):
        """Set all LEDs to one color."""
        if not self._strip:
            logger.debug(f"LEDs → ({r},{g},{b})")
            return
        for i in range(self.count):
            self._strip.setPixelColor(i, Color(r, g, b))
        self._strip.show()

    def set_color_hex(self, hex_color: str):
        r, g, b = hex_to_rgb(hex_color)
        self.set_all(r, g, b)

    def off(self):
        self.set_all(0, 0, 0)

    def breathe(self, hex_color: str, duration: float = 3.0, cycles: int = 1):
        """Breathing/pulsing effect."""
        r, g, b = hex_to_rgb(hex_color)
        steps = 60
        for _ in range(cycles):
            for step in range(steps):
                t = step / steps
                brightness = (math.sin(t * math.pi * 2 - math.pi / 2) + 1) / 2
                self.set_all(
                    int(r * brightness),
                    int(g * brightness),
                    int(b * brightness),
                )
                time.sleep(duration / steps)

    def rainbow(self, duration: float = 2.0):
        """Rainbow cycle across all LEDs."""
        if not self._strip:
            logger.debug("LEDs → rainbow cycle")
            time.sleep(duration)
            return
        steps = int(duration * 30)
        for step in range(steps):
            for i in range(self.count):
                hue = (i * 256 // self.count + step * 8) % 256
                r, g, b = self._wheel(hue)
                self._strip.setPixelColor(i, Color(r, g, b))
            self._strip.show()
            time.sleep(duration / steps)

    def execute_glow(self, color: str, intensity: float = 0.5):
        """Execute a glow command from the AI brain."""
        if color == "rainbow":
            self.rainbow(2.0)
        else:
            # Scale brightness by intensity
            r, g, b = hex_to_rgb(color)
            r = int(r * intensity)
            g = int(g * intensity)
            b = int(b * intensity)
            self.set_all(r, g, b)

    @staticmethod
    def _wheel(pos: int) -> tuple:
        """Color wheel for rainbow effect."""
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return (0, pos * 3, 255 - pos * 3)

    def cleanup(self):
        self.off()
