# ORB — Emotional Companion Robot

## 1. Project Title, Team Members, & Category

**Project Title:** ORB — Emotional Companion Ball

**Team Name:** ORB Robotics

**Team Members:** Hamza Harb, Kaiyuan Duan

**Category/Industry:** Consumer Robotics / Mental Health & Wellness

---

## 2. Problem Statement

Loneliness and emotional neglect are growing crises — over 60% of young adults report feeling seriously lonely (Harvard, 2021). Existing solutions are either purely digital (chatbots, apps) or prohibitively expensive (therapy, companion robots like LOVOT at $3,000+). There is no affordable, physical companion that can detect how you're feeling and respond on its own without being asked.

---

## 3. Solution

ORB is a small robot ball, built from scratch, that listens to your voice tone, detects when you're feeling down, and physically rolls over to comfort you — no commands needed. The MVP focuses on one core interaction: **detecting sadness through vocal tone analysis and autonomously responding with movement, light, and a short spoken comfort message.** It uses a pendulum-drive mechanism inside a clear globe, a Raspberry Pi for on-device audio processing, and a cloud LLM for decision-making.

---

## 4. Target Market

Young adults (18–30) living alone or in dorms who experience loneliness, stress, or anxiety — approximately 33 million single-person households in the U.S. alone. Secondary market: elderly individuals living independently (14.7 million in the U.S.).

---

## 5. Why It's Valuable

A phone notification saying "you seem sad" is easy to ignore. A glowing ball that rolls up to your feet and says "I'm here" is not. ORB bridges the gap between digital emotional support and physical presence at a fraction of the cost of existing companion robots.

---

## 6. How You'll Make Money

**Direct-to-consumer hardware sales** at a target price of $149–$199 per unit (BOM ~$79, healthy margin at scale). Recurring revenue through a **companion subscription** ($5/mo) for premium AI personality, mood history tracking, and advanced emotional responses. Free tier works out of the box with basic comfort behaviors.

---

## 7. MVP Features

- **Custom-built pendulum-drive ball** — clear acrylic globe, 2 motors, counterweight steering, built entirely from scratch
- **Voice tone emotion detection** — on-device pitch and energy analysis via MEMS microphone (not speech-to-text, just tone)
- **Autonomous comfort response** — ball rolls toward user, glows warm amber, speaks a short comfort message
- **LED mood expression** — NeoPixel ring displays breathing patterns mapped to detected/current emotional state
- **Cloud AI decision engine** — receives mood label + context, returns a physical action (move, glow, speak, or stay quiet)
- **Idle presence behavior** — soft breathing glow when no emotion detected, gentle nudge after prolonged silence

---

## 8. Timeline & Division of Work

| Week | Milestone | Harb | Kaiyuan |
|------|-----------|------|---------|
| 1–2 | Hardware assembly — pendulum drive, motor wiring, globe mounting | Motor driver + Pi wiring | Pendulum mechanism + chassis |
| 3–4 | Basic movement — forward, backward, turning, calibration | Motor control software (Python GPIO) | IMU integration + movement tuning |
| 5–6 | Emotion detection — mic input, pitch/energy classifier | Audio pipeline + classifier | Cloud AI integration (Claude API) |
| 7–8 | Response system — LED patterns, speaker output, comfort messages | LED mood mapping + animations | TTS integration + message design |
| 9 | Integration testing — full loop from detection to physical response | End-to-end testing | Edge case handling + reliability |
| 10 | Demo polish + presentation | Demo script + presentation | Video recording + documentation |

---

## 9. Team Roles & Responsibilities

**Hamza Harb** — Lead Developer & Hardware Engineer
- Responsibilities: Motor control software, audio processing pipeline, LED programming, system integration, project architecture
- Estimated codebase contribution: 55%

**Kaiyuan Duan** — Hardware Engineer & AI Integration
- Responsibilities: Pendulum drive mechanical assembly, IMU calibration, cloud AI decision engine, TTS integration, testing
- Estimated codebase contribution: 45%

---

## 10. Viability (How We'll Prove This Works)

**User Testing:** Live demo with 5–10 classmates. User sits near ORB, speaks naturally, and we measure: (1) did ORB correctly detect the emotion? (2) did the physical response feel appropriate? (3) subjective comfort rating 1–10.

**Competitive Analysis:**
| Product | Price | Physical? | Emotion Detection? | Autonomous? |
|---------|-------|-----------|-------------------|-------------|
| Replika (app) | Free/$20/mo | ❌ | Text-based only | ❌ |
| Woebot (app) | Free | ❌ | Text-based only | ❌ |
| LOVOT (robot) | $3,000+ | ✅ | Camera-based | ✅ |
| Moflin (pet robot) | $400 | ✅ | Touch only | Partial |
| **ORB** | **~$150** | **✅** | **Voice tone** | **✅** |

ORB is the only product under $200 that combines physical presence, voice-based emotion detection, and autonomous response.

**Success Metrics:** >70% emotion detection accuracy on sad/neutral/happy classification. >7/10 average comfort rating from test users.

---

## 11. Scalability

**Phase 1 — Now (MVP):** Single emotion (sadness), single response (comfort), pendulum drive in clear globe. Prove the concept works.

**Phase 2 — 6 Months:** Multi-emotion detection (happy, stressed, angry, lonely). Multiple response behaviors. Companion app for mood history and personality customization. Refined industrial design.

**Phase 3 — 12 Months:** On-device SLM (small language model) for offline operation. Camera module for facial expression detection. Mass production via injection molding. Launch on Kickstarter/Indiegogo targeting $100K.

**Phase 4 — 18+ Months:** Enterprise vertical — elderly care facilities, therapy offices, children's hospitals. API for third-party developers to build custom companion behaviors.

---

## 12. Sources & References

- Harvard Graduate School of Education (2021). "Loneliness in America." https://mcc.gse.harvard.edu/reports/loneliness-in-america
- U.S. Census Bureau. "Single-person households." https://www.census.gov/library/visualizations/interactive/living-alone.html
- Administration for Community Living. "Profile of Older Americans." https://acl.gov/aging-and-disability-in-america/data-and-research/profile-older-americans
- LOVOT Robotics. Product page. https://lovot.life/en/
- Moflin. Product page. https://moflin.com/
- Replika AI. https://replika.com/
- Woebot Health. https://woebothealth.com/
