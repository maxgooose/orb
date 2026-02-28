"""Tests for the brain module (offline/fallback mode)."""
import pytest
from orb.brain.claude_brain import ClaudeBrain, OrbAction
from orb.utils.mood_history import MoodHistory


def test_default_actions():
    for mood in ("sad", "happy", "stressed", "silent", "neutral"):
        action = OrbAction.default_for_mood(mood)
        assert isinstance(action, OrbAction)
        assert action.movement in ("toward", "away", "circle", "nudge", "still")


def test_brain_fallback():
    """Without API key, brain should use fallback actions."""
    history = MoodHistory()
    brain = ClaudeBrain(history)
    action = brain.decide("sad", 0.8)
    assert action.movement == "toward"
    assert action.message  # Should have a comfort message


def test_mood_history_integration():
    history = MoodHistory()
    brain = ClaudeBrain(history)
    brain.decide("neutral", 0.5)
    brain.decide("sad", 0.7)
    assert history.current == "sad"
    assert len(history.recent) == 2
