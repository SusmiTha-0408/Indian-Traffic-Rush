# 🏎️ INDIAN TRAFFIC RUSH
## Game Design Document — Version 1.0

---

## 1. Game Overview
- **Game Name:** Indian Traffic Rush
- **Genre:** Racing / Endless Traffic Dodging
- **Platform:** Desktop (Python / Pygame)
- **Game Type:** Single Player
- **Perspective:** Top-down / 2D racing view
- **Target:** A simple, fun, beginner-friendly racing game that can later be expanded with advanced features.

---

## 2. Main Game Concept
The player controls a racing car on a busy Indian-style road.
The road continuously moves downward to create the feeling that the player's car is moving forward.

The player must:
- Avoid traffic vehicles.
- Collect coins.
- Use Nitro Boost.
- Survive for as long as possible.
- Achieve the highest possible score.

The game becomes progressively harder as the player's score increases.

---

## 3. Core Gameplay Loop
```text
START GAME -> PLAYER CAR APPEARS -> ROAD STARTS MOVING -> TRAFFIC VEHICLES SPAWN -> PLAYER DODGES TRAFFIC -> PLAYER COLLECTS COINS -> SCORE INCREASES -> COLLISION? -> GAME OVER
```

---

## 4. Main Features
- **Feature 1 — Traffic Dodging:** Avoid Cars, Buses, Bikes, and Auto Rickshaws.
- **Feature 2 — Nitro Boost:** Speed boost activated via SPACE bar with rechargable meter.
- **Feature 3 — Coins:** Collect coins on road for extra score and economy.

---

## 5. Controls
- **LEFT ARROW / A:** Move Left
- **RIGHT ARROW / D:** Move Right
- **SPACE:** Activate Nitro
- **ESC:** Return to Menu or Quit
