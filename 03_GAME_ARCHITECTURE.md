# 03 - GAME ARCHITECTURE
# Indian Traffic Rush

## 1. Purpose
This document defines the technical architecture of the Indian Traffic Rush game.
The game is developed using Python and Pygame with a modular architecture so four team members can develop features independently.

## 2. Core Architecture Flow
```text
Player Input
     ↓
Game Loop (60 FPS)
     ↓
Game State Update (MENU / PLAYING / GAME_OVER)
     ↓
Player / Traffic / Coins / Nitro
     ↓
Collision Detection (AABB Rect)
     ↓
Score & Game State
     ↓
Rendering
     ↓
Display Flip
```

## 3. Team Responsibilities
- **Member 1 (Core / Player):** `main.py`, `game.py`, `player.py`
- **Member 2 (Traffic):** `traffic.py`
- **Member 3 (Coins / Nitro):** `coins.py`, `nitro.py`
- **Member 4 (UI / Testing):** `ui.py`
