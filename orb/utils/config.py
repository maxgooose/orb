"""Configuration loader for ORB."""
import os
import yaml
from pathlib import Path

_config = None

def reset():
    """Reset cached config (useful for testing)."""
    global _config
    _config = None

def load_config(path: str = None) -> dict:
    """Load YAML config. Searches: explicit path → ORB_CONFIG env → ./config.yaml"""
    global _config
    if _config is not None:
        return _config

    if path is None:
        path = os.environ.get("ORB_CONFIG")
    if path is None:
        # Walk up from this file to find config.yaml
        candidates = [
            Path.cwd() / "config.yaml",
            Path(__file__).parent.parent.parent / "config.yaml",
        ]
        for c in candidates:
            if c.exists():
                path = str(c)
                break

    if path is None or not Path(path).exists():
        # No config file — use empty dict so get() defaults work
        _config = {}
        return _config

    with open(path, "r") as f:
        _config = yaml.safe_load(f) or {}
    return _config


def get(key: str, default=None):
    """Get a nested config value using dot notation: 'claude.api_key'"""
    cfg = load_config()
    parts = key.split(".")
    val = cfg
    for p in parts:
        if isinstance(val, dict):
            val = val.get(p)
        else:
            return default
        if val is None:
            return default
    return val
