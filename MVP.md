# ORB — Emotional Companion Ball
## MVP Spec (One Page)

### What It Is
A rolling ball that senses your emotional state and physically comes to you with comfort. It glows, moves, and speaks — not because you told it to, but because it *noticed*.

### Core Loop
```
Detect Emotion → Decide Response → Act Physically
```

**Detect:** Mic picks up voice tone (not words — tone). Sad/stressed voice = low pitch, slow cadence, sighs. Happy = higher energy, laughter. Silence for too long = lonely.

**Decide:** AI brain (cloud LLM) receives: emotion label + context (time of day, how long since last interaction, recent mood history). Decides what to do.

**Act:**
- 🔵 Sad detected → ball slowly rolls toward user, glows warm amber, plays a soft hum, then speaks a short comfort message ("Hey. I'm here.")
- 🟢 Happy detected → ball spins in a little circle, flashes bright colors, chirps
- 🟡 Silence too long → ball nudges user's foot, pulses a gentle light, waits
- 🔴 Stress/anger detected → ball backs away slightly, dims to a calm blue, says nothing — just glows quietly nearby

### Hardware (DIY Pendulum Drive)
| Part | Cost |
|---|---|
| Clear acrylic globe 15cm | $15 |
| Raspberry Pi Zero 2W | $15 |
| 2x micro gear motors + L298N driver | $11 |
| I2S MEMS microphone | $5 |
| Small speaker + I2S amp | $7 |
| NeoPixel LED ring (16 LEDs) | $6 |
| IMU (MPU6050) | $3 |
| LiPo battery 3.7V 2000mAh + charger | $12 |
| Counterweight + mounting hardware | $5 |
| **Total** | **~$79** |

### Software Stack
- **Pi Zero 2W** runs Python
- **Audio emotion detection:** lightweight classifier on-device (speech_recognition + simple pitch/energy analysis, no heavy ML needed for MVP)
- **AI brain:** Claude API via WiFi. Prompt: "You are Orb, an emotional companion. Given the user's detected mood [{mood}], time [{time}], and mood history [{history}], decide ONE action: comfort, celebrate, nudge, or quiet-presence. Respond with: movement (toward/away/circle/still), glow color, and a short message (max 10 words) or silence."
- **Motor control:** simple Python GPIO, forward/back/turn
- **LED control:** NeoPixel library, mood-mapped color palettes
- **Speaker:** pyttsx3 or ElevenLabs TTS for warmth

### What Makes It Special
It's not a chatbot in a ball. It doesn't wait for commands. It **observes and acts on its own**. The emotional intelligence is the product — the ball just makes it physical.

A phone app can detect your mood too. But it can't roll up to you and glow.

### Demo Script (2 minutes)
1. Ball sits idle, breathing a soft blue glow
2. User sits nearby, sighs, says something in a tired/sad voice
3. Ball detects low mood → slowly rolls toward user
4. Glows warm amber → says "Rough day? I'm right here."
5. User laughs → ball spins, flashes colors, chirps
6. User goes quiet for 30 seconds → ball gently nudges, pulses light
7. End: "Orb doesn't just hear you. It feels you."

### Build Order
1. **Week 1-2:** Assemble ball, get it rolling reliably (motors + Pi + pendulum)
2. **Week 3-4:** Add mic + emotion detection (pitch/energy classifier)
3. **Week 5-6:** Wire AI brain (Claude API → decision → motor/LED commands)
4. **Week 7-8:** Add speaker + comfort messages + personality tuning
5. **Week 9-10:** Polish — smooth movements, LED transitions, demo prep
