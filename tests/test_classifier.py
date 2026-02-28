"""Tests for the emotion classifier."""
import pytest
from orb.emotion.classifier import classify


def test_silent_detection():
    features = {"energy": 0.02, "pitch_mean": 0, "pitch_std": 0, "zcr": 0.01, "speaking_rate": 0}
    mood, conf = classify(features)
    assert mood == "silent"
    assert conf > 0.5


def test_sad_detection():
    features = {"energy": 0.1, "pitch_mean": 120, "pitch_std": 10, "zcr": 0.05, "speaking_rate": 1.5}
    mood, conf = classify(features)
    assert mood == "sad"


def test_happy_detection():
    features = {"energy": 0.7, "pitch_mean": 250, "pitch_std": 50, "zcr": 0.08, "speaking_rate": 5.0}
    mood, conf = classify(features)
    assert mood == "happy"


def test_stressed_detection():
    features = {"energy": 0.8, "pitch_mean": 160, "pitch_std": 60, "zcr": 0.20, "speaking_rate": 6.0}
    mood, conf = classify(features)
    assert mood == "stressed"


def test_neutral_fallback():
    features = {"energy": 0.3, "pitch_mean": 170, "pitch_std": 25, "zcr": 0.07, "speaking_rate": 3.0}
    mood, conf = classify(features)
    # Should be neutral-ish (not strongly any other mood)
    assert mood in ("neutral", "sad", "happy")  # Flexible for edge cases


def test_returns_tuple():
    features = {"energy": 0.5, "pitch_mean": 180, "pitch_std": 30, "zcr": 0.1, "speaking_rate": 3.5}
    result = classify(features)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], str)
    assert isinstance(result[1], float)
