"""
Rule-based emotion classifier using audio features.
Maps pitch, energy, speaking rate → mood label.

This is intentionally simple for the MVP. A trained model can replace it later.
"""
import logging
from typing import Dict, Tuple
from ..utils.config import get

logger = logging.getLogger("orb.emotion")

# Mood labels
MOODS = ("sad", "happy", "stressed", "neutral", "silent")


def classify(features: Dict[str, float]) -> Tuple[str, float]:
    """
    Classify emotional state from audio features.
    
    Returns:
        (mood, confidence) where mood is one of MOODS and confidence is 0.0–1.0
    """
    energy = features.get("energy", 0.0)
    pitch = features.get("pitch_mean", 0.0)
    pitch_std = features.get("pitch_std", 0.0)
    zcr = features.get("zcr", 0.0)
    speaking_rate = features.get("speaking_rate", 0.0)

    sad_pitch_max = get("emotion.sad_pitch_max", 150)
    happy_pitch_min = get("emotion.happy_pitch_min", 200)
    energy_threshold = get("emotion.energy_threshold", 0.3)

    # No voice detected
    if energy < 0.05 or pitch == 0.0:
        return ("silent", 0.9)

    scores = {
        "sad": 0.0,
        "happy": 0.0,
        "stressed": 0.0,
        "neutral": 0.0,
    }

    # --- Sad indicators ---
    # Low pitch, low energy, slow speaking
    if pitch < sad_pitch_max:
        scores["sad"] += 0.3
    if energy < energy_threshold:
        scores["sad"] += 0.3
    if speaking_rate < 2.0:
        scores["sad"] += 0.2
    if pitch_std < 20:  # Monotone
        scores["sad"] += 0.2

    # --- Happy indicators ---
    # High pitch, high energy, fast speaking, variable pitch
    if pitch > happy_pitch_min:
        scores["happy"] += 0.3
    if energy > energy_threshold * 1.5:
        scores["happy"] += 0.2
    if speaking_rate > 4.0:
        scores["happy"] += 0.2
    if pitch_std > 40:  # Expressive
        scores["happy"] += 0.3

    # --- Stressed indicators ---
    # High energy but low/variable pitch, fast rate
    if energy > energy_threshold * 1.5 and pitch < happy_pitch_min:
        scores["stressed"] += 0.3
    if speaking_rate > 5.0:
        scores["stressed"] += 0.2
    if zcr > 0.15:  # Harsh/noisy voice
        scores["stressed"] += 0.2
    if pitch_std > 50 and energy > energy_threshold:
        scores["stressed"] += 0.3

    # --- Neutral baseline ---
    scores["neutral"] = 0.3  # Always a baseline

    # Pick highest score
    mood = max(scores, key=scores.get)
    confidence = min(scores[mood], 1.0)

    # Low confidence → default to neutral
    if confidence < 0.3:
        mood = "neutral"
        confidence = 0.5

    logger.debug(
        f"Classification: {mood} ({confidence:.0%}) | "
        f"pitch={pitch:.0f}Hz energy={energy:.2f} rate={speaking_rate:.1f}"
    )
    return (mood, confidence)


if __name__ == "__main__":
    """Test with synthetic feature vectors."""
    test_cases = [
        {"energy": 0.1, "pitch_mean": 120, "pitch_std": 10, "zcr": 0.05, "speaking_rate": 1.5},  # sad
        {"energy": 0.7, "pitch_mean": 250, "pitch_std": 50, "zcr": 0.08, "speaking_rate": 5.0},  # happy
        {"energy": 0.8, "pitch_mean": 160, "pitch_std": 60, "zcr": 0.20, "speaking_rate": 6.0},  # stressed
        {"energy": 0.3, "pitch_mean": 170, "pitch_std": 25, "zcr": 0.07, "speaking_rate": 3.0},  # neutral
        {"energy": 0.02, "pitch_mean": 0, "pitch_std": 0, "zcr": 0.01, "speaking_rate": 0.0},    # silent
    ]
    for features in test_cases:
        mood, conf = classify(features)
        print(f"  {mood:>10} ({conf:.0%}) ← {features}")
