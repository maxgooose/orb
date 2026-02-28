"""Tests for motor control (simulation mode)."""
import pytest
from orb.hardware.motors import Motors


def test_motor_setup():
    m = Motors()
    m.setup()
    assert m._initialized


def test_execute_movement():
    m = Motors()
    m.setup()
    # Should not raise in simulation mode
    m.execute_movement("toward", 0.5)
    m.execute_movement("away", 0.3)
    m.execute_movement("circle", 0.8)
    m.execute_movement("nudge", 0.4)
    m.execute_movement("still", 0.1)
    m.cleanup()
