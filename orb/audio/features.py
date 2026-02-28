"""
Audio feature extraction for emotion detection.
Extracts pitch (F0), energy, spectral centroid, and speaking rate.
"""
import numpy as np
import logging
from typing import Dict, Optional
from ..utils.config import get

logger = logging.getLogger("orb.audio")

try:
    import librosa
    HAS_LIBROSA = True
except ImportError:
    HAS_LIBROSA = False
    logger.warning("librosa not available — feature extraction will use basic numpy")


def extract_features(audio: np.ndarray, sr: int = None) -> Dict[str, float]:
    """
    Extract emotion-relevant audio features from a numpy array.
    
    Returns:
        pitch_mean: Average fundamental frequency (Hz)
        pitch_std: Pitch variability
        energy: RMS energy (normalized 0-1)
        spectral_centroid: Brightness of sound
        zcr: Zero-crossing rate (correlates with noisiness)
        speaking_rate: Estimated syllables per second
    """
    if sr is None:
        sr = get("audio.sample_rate", 16000)

    audio_float = audio.astype(np.float32) / 32768.0  # Normalize int16 to float

    features = {}

    # Energy (RMS)
    rms = np.sqrt(np.mean(audio_float ** 2))
    features["energy"] = float(min(rms * 10, 1.0))  # Scale to ~0-1

    # Zero-crossing rate
    zcr = np.mean(np.abs(np.diff(np.sign(audio_float)))) / 2
    features["zcr"] = float(zcr)

    if HAS_LIBROSA:
        # Pitch (F0) using librosa
        try:
            f0, voiced_flag, _ = librosa.pyin(
                audio_float, fmin=50, fmax=500, sr=sr
            )
            voiced_f0 = f0[voiced_flag] if voiced_flag is not None else f0[~np.isnan(f0)]
            if len(voiced_f0) > 0:
                features["pitch_mean"] = float(np.mean(voiced_f0))
                features["pitch_std"] = float(np.std(voiced_f0))
            else:
                features["pitch_mean"] = 0.0
                features["pitch_std"] = 0.0
        except Exception:
            features["pitch_mean"] = 0.0
            features["pitch_std"] = 0.0

        # Spectral centroid
        try:
            cent = librosa.feature.spectral_centroid(y=audio_float, sr=sr)
            features["spectral_centroid"] = float(np.mean(cent))
        except Exception:
            features["spectral_centroid"] = 0.0
    else:
        # Basic pitch estimation via autocorrelation
        features["pitch_mean"] = _estimate_pitch_basic(audio_float, sr)
        features["pitch_std"] = 0.0
        features["spectral_centroid"] = 0.0

    # Speaking rate estimate (based on energy envelope peaks)
    features["speaking_rate"] = _estimate_speaking_rate(audio_float, sr)

    return features


def _estimate_pitch_basic(audio: np.ndarray, sr: int) -> float:
    """Simple autocorrelation pitch estimation (fallback without librosa)."""
    if len(audio) < sr // 50:  # Need at least 20ms
        return 0.0

    # Autocorrelation
    corr = np.correlate(audio, audio, mode="full")
    corr = corr[len(corr) // 2:]

    # Find first peak after the initial decline
    min_lag = sr // 500  # 500 Hz max
    max_lag = sr // 50   # 50 Hz min

    if max_lag >= len(corr):
        return 0.0

    segment = corr[min_lag:max_lag]
    if len(segment) == 0:
        return 0.0

    peak_idx = np.argmax(segment) + min_lag
    if peak_idx == 0:
        return 0.0

    return float(sr / peak_idx)


def _estimate_speaking_rate(audio: np.ndarray, sr: int) -> float:
    """Estimate syllables/sec from energy envelope peaks."""
    # Compute envelope
    frame_length = int(0.025 * sr)  # 25ms frames
    hop = int(0.010 * sr)           # 10ms hop

    n_frames = max(1, (len(audio) - frame_length) // hop + 1)
    envelope = np.zeros(n_frames)
    for i in range(n_frames):
        start = i * hop
        end = start + frame_length
        if end <= len(audio):
            envelope[i] = np.sqrt(np.mean(audio[start:end] ** 2))

    if len(envelope) < 3:
        return 0.0

    # Count peaks in envelope (simple: local maxima above mean)
    mean_env = np.mean(envelope)
    peaks = 0
    for i in range(1, len(envelope) - 1):
        if envelope[i] > envelope[i-1] and envelope[i] > envelope[i+1] and envelope[i] > mean_env:
            peaks += 1

    duration = len(audio) / sr
    return peaks / duration if duration > 0 else 0.0
