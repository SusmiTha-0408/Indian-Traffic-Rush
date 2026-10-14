"""
Indian Traffic Rush — Difficulty Module
Manages progressive difficulty scaling based on survival score:
- Difficulty levels (Level 1 to Level 5)
- Speed multipliers
- Traffic spawn interval progression
- Level-up transition notifications
"""

# ========================================================
# DIFFICULTY CONFIGURATION TIERS
# ========================================================
DIFFICULTY_TIERS = [
    {"level": 1, "min_score": 0.0,    "max_score": 199.999, "multiplier": 1.00, "spawn_interval": 2.00},
    {"level": 2, "min_score": 200.0,  "max_score": 499.999, "multiplier": 1.10, "spawn_interval": 1.70},
    {"level": 3, "min_score": 500.0,  "max_score": 999.999, "multiplier": 1.20, "spawn_interval": 1.45},
    {"level": 4, "min_score": 1000.0, "max_score": 1499.999, "multiplier": 1.30, "spawn_interval": 1.20},
    {"level": 5, "min_score": 1500.0, "max_score": float("inf"), "multiplier": 1.40, "spawn_interval": 1.00},
]


class DifficultyManager:
    """Tracks and calculates current difficulty level, multiplier, and spawn rate."""

    def __init__(self):
        self.current_level = 1
        self.current_multiplier = 1.00
        self.current_spawn_interval = 2.00
        self.banner_timer = 0.0
        self.banner_text = ""

    def reset(self):
        """Reset difficulty back to Level 1 with 1.0 multiplier."""
        self.current_level = 1
        self.current_multiplier = 1.00
        self.current_spawn_interval = 2.00
        self.banner_timer = 0.0
        self.banner_text = ""

    def update(self, current_score: float, dt: float):
        """
        Evaluate score against difficulty tiers and advance transition timer.
        :param current_score: Player's current game score
        :param dt: Delta time in seconds
        """
        # Determine matching tier
        active_tier = DIFFICULTY_TIERS[0]
        for tier in DIFFICULTY_TIERS:
            if current_score >= tier["min_score"]:
                active_tier = tier

        # Check for level up transition
        if active_tier["level"] > self.current_level:
            self.current_level = active_tier["level"]
            self.banner_text = f"LEVEL {self.current_level}"
            self.banner_timer = 1.0  # Show transition banner for ~1.0 second

        self.current_multiplier = active_tier["multiplier"]
        self.current_spawn_interval = active_tier["spawn_interval"]

        # Decay transition notification banner timer
        if self.banner_timer > 0.0:
            self.banner_timer = max(0.0, self.banner_timer - dt)
            if self.banner_timer == 0.0:
                self.banner_text = ""
