"""
ORB Demo Mode — runs the full emotional response loop with simulated audio.

No hardware required. Great for:
- Testing the AI brain decisions
- Demonstrating the concept in class
- Development on non-Pi machines

Usage:
    python -m orb.demo
    python -m orb.demo --mood sad
    python -m orb.demo --interactive
"""

import argparse
import time
import random
import sys
from datetime import datetime

# Simulated audio features for each mood
MOOD_PROFILES = {
    'sad': {
        'pitch_mean': 130.0,
        'pitch_std': 8.0,
        'energy': 0.15,
        'spectral_centroid': 1200.0,
        'zcr': 0.04,
        'speaking_rate': 2.5,
    },
    'happy': {
        'pitch_mean': 240.0,
        'pitch_std': 35.0,
        'energy': 0.65,
        'spectral_centroid': 3200.0,
        'zcr': 0.09,
        'speaking_rate': 5.5,
    },
    'stressed': {
        'pitch_mean': 200.0,
        'pitch_std': 40.0,
        'energy': 0.70,
        'spectral_centroid': 3800.0,
        'zcr': 0.12,
        'speaking_rate': 6.0,
    },
    'neutral': {
        'pitch_mean': 170.0,
        'pitch_std': 20.0,
        'energy': 0.35,
        'spectral_centroid': 2200.0,
        'zcr': 0.06,
        'speaking_rate': 4.0,
    },
    'silent': {
        'pitch_mean': 0.0,
        'pitch_std': 0.0,
        'energy': 0.01,
        'spectral_centroid': 0.0,
        'zcr': 0.0,
        'speaking_rate': 0.0,
    },
}

# Color names for terminal display
MOOD_COLORS = {
    'sad': '\033[33m● Warm Amber\033[0m',
    'happy': '\033[96m● Rainbow\033[0m',
    'stressed': '\033[34m● Calm Blue\033[0m',
    'neutral': '\033[37m● Breathing White\033[0m',
    'silent': '\033[35m● Soft Pulse\033[0m',
}

MOOD_MOVEMENTS = {
    'sad': 'Rolling toward user (comfort approach)',
    'happy': 'Spinning in a celebratory circle',
    'stressed': 'Backing away gently (giving space)',
    'neutral': 'Staying nearby, idle',
    'silent': 'Gentle nudge forward',
}

MOOD_SOUNDS = {
    'sad': '"Hey. I\'m here."',
    'happy': '♪ Cheerful chirp ♪',
    'stressed': '(Quiet glow, no speech)',
    'neutral': '(Idle hum)',
    'silent': '(Subtle attention hum)',
}


def add_noise(features: dict) -> dict:
    """Add slight randomness to simulated features for realism."""
    noisy = {}
    for k, v in features.items():
        if isinstance(v, float) and v > 0:
            noise = random.gauss(0, v * 0.1)
            noisy[k] = max(0, v + noise)
        else:
            noisy[k] = v
    return noisy


def classify_mood(features: dict) -> tuple[str, float]:
    """Simplified classifier matching the real one's logic."""
    energy = features.get('energy', 0)
    pitch = features.get('pitch_mean', 0)
    pitch_var = features.get('pitch_std', 0)
    zcr = features.get('zcr', 0)

    if energy < 0.03:
        return 'silent', 0.95

    if pitch < 150 and energy < 0.3:
        return 'sad', 0.7 + min(0.25, (150 - pitch) / 200)

    if pitch > 200 and energy > 0.5 and pitch_var > 25:
        return 'happy', 0.65 + min(0.3, energy * 0.3)

    if energy > 0.55 and zcr > 0.08:
        return 'stressed', 0.6 + min(0.3, zcr * 2)

    return 'neutral', 0.5


def display_response(mood: str, confidence: float, features: dict, cycle: int):
    """Pretty-print the ORB's response."""
    timestamp = datetime.now().strftime('%H:%M:%S')
    
    print(f'\n{"="*60}')
    print(f'  ORB Cycle #{cycle}  |  {timestamp}')
    print(f'{"="*60}')
    print(f'  Audio Features:')
    print(f'    Pitch:    {features["pitch_mean"]:.0f} Hz (±{features["pitch_std"]:.0f})')
    print(f'    Energy:   {"█" * int(features["energy"] * 20):<20s} {features["energy"]:.2f}')
    print(f'    Rate:     {features["speaking_rate"]:.1f} syl/s')
    print(f'  ─────────────────────────────────────')
    print(f'  Detected:  {mood.upper()} ({confidence:.0%} confidence)')
    print(f'  ─────────────────────────────────────')
    print(f'  Response:')
    print(f'    💡 LEDs:     {MOOD_COLORS[mood]}')
    print(f'    🔄 Movement: {MOOD_MOVEMENTS[mood]}')
    print(f'    🔊 Sound:    {MOOD_SOUNDS[mood]}')
    print(f'{"="*60}')


def try_claude_brain(mood: str, confidence: float) -> dict | None:
    """Try to get a response from Claude brain if configured."""
    try:
        from orb.utils.config import load_config
        from orb.brain.claude_brain import ClaudeBrain
        
        config = load_config()
        brain = ClaudeBrain(config)
        action = brain.decide(mood, confidence, [])
        return action
    except Exception:
        return None


def run_single(mood: str, cycle: int = 1):
    """Run a single demo cycle for a given mood."""
    features = add_noise(MOOD_PROFILES[mood])
    detected_mood, confidence = classify_mood(features)
    display_response(detected_mood, confidence, features, cycle)


def run_sequence():
    """Run a full emotional arc: neutral → sad → comfort → happy."""
    print('\n🔮 ORB Demo — Emotional Arc Simulation')
    print('Simulating a person\'s mood shifting over time...\n')
    
    arc = [
        ('neutral', 'Person enters room, talking normally'),
        ('neutral', 'Continuing casual conversation'),
        ('sad', 'Voice drops — something is wrong'),
        ('sad', 'Still low energy, ORB approaches'),
        ('sad', 'ORB is nearby, glowing warm amber'),
        ('neutral', 'Mood lifting slightly'),
        ('happy', 'Laughing now — ORB celebrates'),
        ('neutral', 'Settling back to calm'),
        ('silent', 'Quiet for a while...'),
        ('neutral', 'Back to normal'),
    ]
    
    for i, (mood, narration) in enumerate(arc, 1):
        print(f'\n  📖 {narration}')
        time.sleep(1)
        run_single(mood, cycle=i)
        time.sleep(1.5)
    
    print('\n✅ Demo complete. ORB responded to the full emotional arc.')


def run_interactive():
    """Interactive mode — user picks moods manually."""
    print('\n🔮 ORB Interactive Demo')
    print('Type a mood (sad/happy/stressed/neutral/silent) or "quit" to exit.\n')
    
    cycle = 0
    while True:
        try:
            mood = input('  Mood > ').strip().lower()
        except (EOFError, KeyboardInterrupt):
            break
        
        if mood in ('quit', 'exit', 'q'):
            break
        
        if mood not in MOOD_PROFILES:
            print(f'  Unknown mood. Choose: {", ".join(MOOD_PROFILES.keys())}')
            continue
        
        cycle += 1
        run_single(mood, cycle)


def main():
    parser = argparse.ArgumentParser(description='ORB Demo — simulate emotional companion responses')
    parser.add_argument('--mood', choices=list(MOOD_PROFILES.keys()),
                        help='Run a single mood cycle')
    parser.add_argument('--interactive', '-i', action='store_true',
                        help='Interactive mode — pick moods manually')
    parser.add_argument('--arc', action='store_true',
                        help='Run full emotional arc simulation (default)')
    
    args = parser.parse_args()
    
    if args.mood:
        print(f'\n🔮 ORB Demo — Single mood: {args.mood}')
        run_single(args.mood)
    elif args.interactive:
        run_interactive()
    else:
        run_sequence()


if __name__ == '__main__':
    main()
