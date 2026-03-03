# ORB — Emotional Companion Ball

A rolling robot ball that detects your emotional state through voice tone and physically responds with movement, light, and comfort messages — without being asked.

**Team:** Hamza Harb & Kaiyuan Duan (ORB Robotics)  
**Course:** CS291, Pace University  

## How It Works

```
Voice Tone → Emotion Detection → AI Decision → Physical Response
```

1. **Microphone** captures ambient audio
2. **On-device classifier** detects emotional state (sad, happy, stressed, neutral, silent)
3. **Cloud AI brain** (Claude API) decides how to respond given mood + context
4. **Motors** roll the ball toward/away from user
5. **LEDs** glow with mood-mapped colors
6. **Speaker** delivers short comfort messages

## Hardware

| Component | Purpose |
|---|---|
| Raspberry Pi Zero 2W | Brain |
| 2x micro gear motors + L298N | Pendulum drive (rolling) |
| I2S MEMS microphone | Audio capture |
| I2S speaker + amplifier | Voice output |
| NeoPixel LED ring (16) | Mood lighting |
| MPU6050 IMU | Orientation sensing |
| 3.7V 2000mAh LiPo | Power |
| 15cm clear acrylic globe | Shell |

**Total BOM: ~$79**

## Software Setup

### Prerequisites
- Raspberry Pi Zero 2W with Raspberry Pi OS Lite
- Python 3.9+
- WiFi configured

### Install
```bash
# Clone repo
git clone https://github.com/maxgooose/orb.git
cd orb

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy config
cp config.example.yaml config.yaml
# Edit config.yaml with your Claude API key and WiFi settings
```

### Run
```bash
# Full system (on Raspberry Pi with hardware)
python -m orb.main

# Demo mode (no hardware required — works on any machine)
python -m orb.demo                # Full emotional arc simulation
python -m orb.demo --mood sad     # Single mood test
python -m orb.demo --interactive  # Pick moods manually

# Individual modules (for testing)
python -m orb.audio.listener      # Test microphone
python -m orb.emotion.classifier  # Test emotion detection
python -m orb.hardware.motors     # Test motors
python -m orb.hardware.leds       # Test LED ring
python -m orb.brain.claude_brain  # Test AI decisions
```

## Project Structure
```
orb/
├── orb/                    # Main package
│   ├── __init__.py
│   ├── main.py             # Core loop: listen → detect → decide → act
│   ├── audio/
│   │   ├── __init__.py
│   │   ├── listener.py     # Mic capture + VAD
│   │   └── features.py     # Pitch, energy, cadence extraction
│   ├── emotion/
│   │   ├── __init__.py
│   │   └── classifier.py   # Mood classification from audio features
│   ├── brain/
│   │   ├── __init__.py
│   │   └── claude_brain.py # Claude API integration + decision engine
│   ├── hardware/
│   │   ├── __init__.py
│   │   ├── motors.py       # L298N motor control (GPIO)
│   │   ├── leds.py         # NeoPixel LED patterns
│   │   ├── speaker.py      # TTS output
│   │   └── imu.py          # MPU6050 orientation
│   └── utils/
│       ├── __init__.py
│       ├── config.py        # YAML config loader
│       └── mood_history.py  # Recent mood tracking
├── tests/
│   ├── test_classifier.py
│   ├── test_brain.py
│   └── test_motors.py
├── config.example.yaml
├── requirements.txt
├── PROPOSAL.md
├── MVP.md
└── README.md
```

## Emotional Responses

| Mood | Movement | Color | Sound |
|---|---|---|---|
| 😢 Sad | Roll toward user | Warm amber | "Hey. I'm here." |
| 😊 Happy | Spin in circle | Rainbow flash | Cheerful chirp |
| 😤 Stressed | Back away slightly | Calm blue | Quiet glow, no speech |
| 😶 Silent too long | Gentle nudge | Soft pulse | Subtle hum |
| 😐 Neutral | Stay nearby | Breathing white | Idle |

## License

MIT
