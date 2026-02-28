"""Track recent mood detections for context-aware AI decisions."""
from collections import deque
from datetime import datetime
from dataclasses import dataclass, field
from typing import List


@dataclass
class MoodEntry:
    mood: str           # "sad", "happy", "stressed", "neutral", "silent"
    confidence: float   # 0.0 - 1.0
    timestamp: datetime = field(default_factory=datetime.now)


class MoodHistory:
    def __init__(self, max_size: int = 10):
        self._history: deque[MoodEntry] = deque(maxlen=max_size)

    def add(self, mood: str, confidence: float = 1.0):
        self._history.append(MoodEntry(mood=mood, confidence=confidence))

    @property
    def recent(self) -> List[MoodEntry]:
        return list(self._history)

    @property
    def current(self) -> str:
        if not self._history:
            return "neutral"
        return self._history[-1].mood

    @property
    def trend(self) -> str:
        """Detect mood trend: 'declining', 'improving', 'stable', 'unknown'."""
        if len(self._history) < 3:
            return "unknown"

        mood_scores = {"sad": -2, "stressed": -1, "silent": 0, "neutral": 1, "happy": 2}
        recent = [mood_scores.get(e.mood, 0) for e in list(self._history)[-5:]]
        avg_first = sum(recent[:len(recent)//2]) / max(len(recent)//2, 1)
        avg_second = sum(recent[len(recent)//2:]) / max(len(recent) - len(recent)//2, 1)

        diff = avg_second - avg_first
        if diff > 0.5:
            return "improving"
        elif diff < -0.5:
            return "declining"
        return "stable"

    def summary(self) -> str:
        """Human-readable summary for the AI brain."""
        if not self._history:
            return "No mood data yet."
        entries = [f"{e.mood}({e.confidence:.0%})" for e in list(self._history)[-5:]]
        return f"Recent moods: {', '.join(entries)} | Trend: {self.trend}"
