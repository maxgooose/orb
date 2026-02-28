"""
AI decision engine using Claude API.
Takes mood + context → decides physical response (movement, LED color, message).
"""
import logging
import json
from datetime import datetime
from dataclasses import dataclass
from typing import Optional
from ..utils.config import get
from ..utils.mood_history import MoodHistory

logger = logging.getLogger("orb.brain")

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


@dataclass
class OrbAction:
    """What the orb should physically do."""
    movement: str       # "toward", "away", "circle", "nudge", "still"
    color: str          # hex color or named: "amber", "blue", "rainbow", "white"
    message: str        # short spoken message, or "" for silence
    intensity: float    # 0.0 (gentle) to 1.0 (energetic)

    @classmethod
    def from_dict(cls, d: dict) -> "OrbAction":
        return cls(
            movement=d.get("movement", "still"),
            color=d.get("color", "white"),
            message=d.get("message", ""),
            intensity=d.get("intensity", 0.5),
        )

    @classmethod
    def default_for_mood(cls, mood: str) -> "OrbAction":
        """Fallback actions when AI is unavailable."""
        defaults = {
            "sad":      cls("toward", "#FFB347", "Hey. I'm here.", 0.3),
            "happy":    cls("circle", "#00FF88", "", 0.8),
            "stressed": cls("away",   "#4A90D9", "", 0.2),
            "silent":   cls("nudge",  "#FFFFFF", "", 0.4),
            "neutral":  cls("still",  "#E8E8FF", "", 0.1),
        }
        return defaults.get(mood, defaults["neutral"])


SYSTEM_PROMPT = """You are Orb, an emotional companion ball. You are small, warm, and physical — not a chatbot.

You receive the user's detected mood, time of day, and recent mood history. You decide ONE physical action.

Respond with JSON only:
{
  "movement": "toward" | "away" | "circle" | "nudge" | "still",
  "color": "<hex color>",
  "message": "<max 10 words, or empty string for silence>",
  "intensity": <0.0 to 1.0>
}

Guidelines:
- Sad: roll toward slowly, warm amber glow, short comforting words
- Happy: spin/circle, bright colors, optional chirp sound (empty message)
- Stressed: back away slightly, calm blue, be a quiet presence (no words)
- Silent too long: gentle nudge, soft pulsing light, brief acknowledgment
- Neutral: stay nearby, gentle breathing light, no message

Be genuine. Not cheesy. Not robotic. Like a pet that just... knows.
Late night (11pm-6am): be extra gentle, lower intensity.
If mood is declining: be more proactive, move closer.
If mood is improving: celebrate subtly, don't overdo it."""


class ClaudeBrain:
    def __init__(self, mood_history: MoodHistory):
        self.mood_history = mood_history
        self._client = None
        self._model = get("claude.model", "claude-sonnet-4-20250514")

        if HAS_ANTHROPIC:
            api_key = get("claude.api_key")
            if api_key:
                self._client = anthropic.Anthropic(api_key=api_key)

    def decide(self, mood: str, confidence: float) -> OrbAction:
        """Given detected mood, decide what the orb should do."""
        self.mood_history.add(mood, confidence)

        # Try Claude API
        if self._client:
            try:
                return self._call_claude(mood, confidence)
            except Exception as e:
                logger.warning(f"Claude API error, using fallback: {e}")

        # Fallback: hardcoded responses
        return OrbAction.default_for_mood(mood)

    def _call_claude(self, mood: str, confidence: float) -> OrbAction:
        now = datetime.now()
        context = {
            "detected_mood": mood,
            "confidence": f"{confidence:.0%}",
            "time": now.strftime("%I:%M %p"),
            "day": now.strftime("%A"),
            "mood_history": self.mood_history.summary(),
            "trend": self.mood_history.trend,
        }

        response = self._client.messages.create(
            model=self._model,
            max_tokens=150,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": json.dumps(context)}],
        )

        text = response.content[0].text.strip()
        # Parse JSON from response (handle markdown code blocks)
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        action_dict = json.loads(text)
        return OrbAction.from_dict(action_dict)


if __name__ == "__main__":
    """Test the brain with a mock mood sequence."""
    logging.basicConfig(level=logging.INFO)
    history = MoodHistory()
    brain = ClaudeBrain(history)

    test_moods = [
        ("neutral", 0.5),
        ("sad", 0.7),
        ("sad", 0.8),
        ("happy", 0.6),
    ]

    for mood, conf in test_moods:
        action = brain.decide(mood, conf)
        print(f"Mood: {mood} ({conf:.0%}) → move={action.movement}, "
              f"color={action.color}, msg='{action.message}', intensity={action.intensity}")
