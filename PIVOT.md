# ORB — Software Pivot Proposal

## What Changed

Professor wants a software project for CS291. The hardware ORB (pendulum-drive companion ball) is parked. But the core idea — **an AI that detects your emotional state and responds without being asked** — is even more powerful as pure software.

## The Pivot

**ORB becomes a web app.** Same emotional intelligence, no hardware required. It runs in any browser, uses your real microphone, and responds with a 3D animated companion + AI-generated comfort messages.

Think of it as: **a mood-aware AI companion that lives in your browser tab.**

## Why This Works Better (for CS291)

- **Everyone can try it** — no hardware to assemble, just open a URL
- **Deploys instantly** — Vercel/Netlify, share a link with the class
- **We already built it** — the 3D simulator IS the product, just needs features
- **Technically richer** — Web Audio API, Three.js 3D rendering, real-time ML, Claude API, PWA, IndexedDB — more CS topics than a Pi project
- **Scalable story** — from browser tab to mobile app to Chrome extension

## Feature Set (Software MVP)

### Already Built ✅
- Three.js 3D translucent orb with particle system
- Real microphone input via Web Audio API
- Voice tone emotion detection (pitch, energy, cadence, ZCR)
- Mood classification: sad, happy, stressed, silent, neutral
- Visual mood responses: color shifts, movement, glow intensity
- Demo mode with scripted emotional arc
- Responsive design (desktop + mobile)

### New for Pivot 🆕
- **Mood Journal** — every session logged with timestamps, mood timeline, and notes
- **Session History** — browse past sessions, see mood patterns over days/weeks
- **AI Comfort Messages** — Claude API generates contextual responses (not hardcoded)
- **Settings Panel** — mic sensitivity, theme, notification preferences
- **PWA (Progressive Web App)** — installable on phone/desktop, works offline
- **Mood Analytics** — charts showing mood distribution, trends, streaks
- **Export** — download mood history as CSV/JSON

## Tech Stack

| Layer | Technology |
|-------|-----------|
| 3D Rendering | Three.js (translucent sphere, particles, volumetric glow) |
| Audio Processing | Web Audio API (real-time FFT, pitch detection, energy analysis) |
| Emotion Classification | Custom JS classifier (pitch + energy + cadence + ZCR → mood) |
| AI Responses | Claude API (mood + context → personalized comfort message) |
| Data Persistence | IndexedDB via idb-keyval (mood sessions, journal entries) |
| Offline Support | Service Worker + Cache API (PWA) |
| Deployment | Vercel (zero-config static deploy) |

## Updated Timeline

| Week | Milestone | Harb | Kaiyuan |
|------|-----------|------|---------|
| 1 | Mood journal + session storage (IndexedDB) | Journal UI + data layer | Session list + history view |
| 2 | AI integration (Claude API for dynamic messages) | API integration + prompt eng | Response UI + speech bubble redesign |
| 3 | Analytics dashboard (mood charts, trends) | Chart.js mood visualizations | Data aggregation + export |
| 4 | PWA + polish (service worker, manifest, install) | PWA setup + offline caching | Settings panel + mic calibration |
| 5 | Testing + demo prep | Integration tests + demo script | User testing + accessibility |

## Demo Script (Updated)

1. Open ORB in browser — orb glows softly, breathing animation
2. Click mic — "ORB is listening"
3. Speak in a tired/sad voice → orb shifts to warm amber, rolls closer, says "Rough day? I'm right here."
4. Laugh → orb spins, flashes green, celebrates
5. Go quiet → orb nudges, pulses gently
6. Open journal → shows today's mood timeline with color-coded entries
7. Open analytics → mood distribution pie chart, weekly trend line
8. "ORB doesn't just hear you. It feels you. Now — everywhere you go."

## Competitive Angle (Updated)

| Product | Platform | Voice Detection | Autonomous | Visual Companion | Mood History |
|---------|----------|----------------|-----------|-----------------|-------------|
| Replika | App | ❌ Text only | ❌ | Avatar (3D) | ❌ |
| Woebot | App | ❌ Text only | ❌ | ❌ | Basic |
| Youper | App | ❌ Text only | ❌ | ❌ | Yes |
| **ORB** | **Web (any device)** | **✅ Real-time voice tone** | **✅** | **✅ 3D orb** | **✅** |

ORB is the only product that detects emotion from **voice tone** (not text), responds **autonomously** (no buttons to press), and provides a **visual physical companion** — all in a browser.
