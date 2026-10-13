# 🏎️ INDIAN TRAFFIC RUSH — Prototype Foundation

Indian Traffic Rush is a 2D top-down highway traffic dodging game built with **Python** and **Pygame**.

This project is organized into clean, independent modules designed for a 4-person development team to collaborate via GitHub branches without code conflicts.

---

## 🛠️ Requirements & Setup

### Prerequisites
- Python 3.9+ (Python 3.10+ recommended)
- `pip`

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Game
```bash
python main.py
```

---

## 🎮 Controls (Stage 1 Foundation)

- **`SPACE` or `ENTER`**: Start Game from Main Menu
- **`LEFT ARROW` or `A`**: Steer Car Left
- **`RIGHT ARROW` or `D`**: Steer Car Right
- **`ESC`**: Pause / Return to Main Menu / Exit
- **`R`**: Restart Game on Game-Over screen

---

## 🏗️ Architecture & Team Responsibilities

```text
main.py
   ↓
game.py
   ↓
 ┌──────────────┐
 │              │
player.py   traffic.py
 │              │
coins.py    nitro.py
 │              │
 └──────┬───────┘
        ↓
      ui.py
```

| Member | Focus | Files | Responsibilities |
| :--- | :--- | :--- | :--- |
| **Member 1** | Core / Player | `main.py`, `game.py`, `player.py` | Pygame init, main loop (60 FPS), road scrolling, player movement & boundaries. |
| **Member 2** | Traffic | `traffic.py` | Traffic vehicles (Bus, Rickshaw, Bike, Car), random spawner, speeds & rectangles. |
| **Member 3** | Coins & Nitro | `coins.py`, `nitro.py` | Collectible coin spawning, score rewards, nitro gauge & boost speed multiplier. |
| **Member 4** | UI & Testing | `ui.py` | HUD rendering (Score, Coins, Nitro meter), Menu screen, Game Over screen, and QA. |

---

## 📁 Project Structure

```text
racing/
│
├── main.py                     # Entry point (creates Game and runs)
├── game.py                     # Main game controller & 60 FPS loop
├── player.py                   # Player car representation, controls & boundaries
├── traffic.py                  # Traffic system module
├── coins.py                    # Collectible coins module
├── nitro.py                    # Nitro boost system module
├── ui.py                       # Menu, HUD & Game Over UI rendering
│
├── assets/
│   ├── images/                 # Image assets (optional for future stages)
│   └── sounds/                 # Sound assets (optional for future stages)
│
├── docs/
│   ├── 01_GAME_DESIGN.md       # Game Design Document (v1.0)
│   ├── 02_SETUP.md             # Detailed developer setup guide
│   └── 03_GAME_ARCHITECTURE.md # Architecture specification & team workflow
│
├── requirements.txt            # Python dependencies (pygame>=2.5.0)
├── README.md                   # Project overview & running instructions
└── .gitignore                  # Git ignore rules for Python & Pygame
```
