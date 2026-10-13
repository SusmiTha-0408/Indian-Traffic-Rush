"""
Indian Traffic Rush — Nitro Module
Member 3: Coins / Nitro

Manages nitro boost capacity, depletion, slow recharge, speed multiplier,
and procedural exhaust flame effects.
"""

import random
import pygame

# ========================================================
# NITRO CONFIGURATION CONSTANTS
# ========================================================
MAX_NITRO = 100.0
INITIAL_NITRO = 100.0
NITRO_DRAIN_PER_SECOND = 35.0
NITRO_RECHARGE_PER_SECOND = 12.0
NITRO_SPEED_MULTIPLIER = 1.8


class NitroSystem:
    def __init__(self):
        self.max_nitro = MAX_NITRO
        self.nitro_amount = INITIAL_NITRO
        self.drain_rate = NITRO_DRAIN_PER_SECOND
        self.recharge_rate = NITRO_RECHARGE_PER_SECOND
        self.speed_multiplier = NITRO_SPEED_MULTIPLIER
        self.is_active = False

        # Visual flame colors
        self.flame_outer_color = (6, 182, 212)    # Electric Cyan
        self.flame_inner_color = (165, 243, 252)  # Bright White-Cyan core

    @property
    def current_nitro(self) -> float:
        """Alias property for nitro_amount for backwards compatibility."""
        return self.nitro_amount

    @current_nitro.setter
    def current_nitro(self, val: float):
        self.nitro_amount = float(val)

    def reset(self):
        """Restore nitro to maximum capacity and deactivate boost."""
        self.nitro_amount = self.max_nitro
        self.is_active = False

    def update(self, is_space_held: bool, dt: float):
        """
        Update nitro status, depletion when active, and recharge when inactive.
        - Nitro activates ONLY while SPACE is physically held and capacity > 0.
        - Releasing SPACE immediately deactivates Nitro.
        - Nitro recharges ONLY while SPACE is NOT held and Nitro is inactive.
        - Nitro NEVER automatically activates while recharging.
        :param is_space_held: True if the player is actively holding SPACE
        :param dt: Delta time in seconds
        """
        if dt <= 0.0:
            return

        if is_space_held:
            if self.nitro_amount > 0.0:
                self.is_active = True
                self.nitro_amount -= self.drain_rate * dt
                if self.nitro_amount <= 0.0:
                    self.nitro_amount = 0.0
                    self.is_active = False
            else:
                # Capacity depleted while SPACE is held: remain inactive, do NOT recharge
                self.nitro_amount = 0.0
                self.is_active = False
        else:
            # Releasing SPACE immediately deactivates Nitro
            self.is_active = False
            # Recharge only while inactive and SPACE is NOT held
            if self.nitro_amount < self.max_nitro:
                self.nitro_amount += self.recharge_rate * dt
                if self.nitro_amount > self.max_nitro:
                    self.nitro_amount = self.max_nitro

    def get_multiplier(self) -> float:
        """Returns the current speed multiplier (1.8 when boosting, 1.0 otherwise)."""
        return self.speed_multiplier if self.is_active else 1.0

    def get_percentage(self) -> float:
        """Returns nitro level ratio between 0.0 and 1.0."""
        return max(0.0, min(1.0, self.nitro_amount / self.max_nitro))

    def draw_effects(self, surface: pygame.Surface, player_rect: pygame.Rect):
        """
        Draw dual exhaust flame boost effects behind the player's car.
        Only rendered while nitro boost is actively engaged.
        """
        if not self.is_active:
            return

        flame_len = random.randint(14, 22)
        inner_len = flame_len - 6

        # Left Exhaust Pipe Flame
        left_x = player_rect.x + 9
        left_outer = [
            (left_x - 3, player_rect.bottom - 2),
            (left_x + 3, player_rect.bottom - 2),
            (left_x, player_rect.bottom + flame_len)
        ]
        left_inner = [
            (left_x - 1, player_rect.bottom - 2),
            (left_x + 1, player_rect.bottom - 2),
            (left_x, player_rect.bottom + inner_len)
        ]
        pygame.draw.polygon(surface, self.flame_outer_color, left_outer)
        pygame.draw.polygon(surface, self.flame_inner_color, left_inner)

        # Right Exhaust Pipe Flame
        right_x = player_rect.right - 9
        right_outer = [
            (right_x - 3, player_rect.bottom - 2),
            (right_x + 3, player_rect.bottom - 2),
            (right_x, player_rect.bottom + flame_len)
        ]
        right_inner = [
            (right_x - 1, player_rect.bottom - 2),
            (right_x + 1, player_rect.bottom - 2),
            (right_x, player_rect.bottom + inner_len)
        ]
        pygame.draw.polygon(surface, self.flame_outer_color, right_outer)
        pygame.draw.polygon(surface, self.flame_inner_color, right_inner)
