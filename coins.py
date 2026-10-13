"""
Indian Traffic Rush — Coins Module
Member 3: Coins / Nitro

Manages collectible coins, procedural coin rendering,
multi-lane spawning, downward road movement, and player collection detection.
"""

import random
import pygame


class Coin:
    """Represents an individual collectible golden coin on the highway."""

    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)
        self.radius = 12
        self.collected = False

        # Color attributes (Golden yellow with darker rim and shine)
        self.color_rim = (202, 138, 4)      # Dark gold border
        self.color_body = (250, 204, 21)    # Bright gold face
        self.color_inner = (234, 179, 8)    # Inner embossed rim
        self.color_shine = (254, 240, 138)  # White-gold highlight

        # Pygame Rect for position and collision detection
        self.rect = pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2
        )

    def update(self, dt: float, road_speed_pps: float):
        """Move coin downward at the road scrolling speed."""
        self.y += road_speed_pps * dt
        self.rect.x = int(self.x - self.radius)
        self.rect.y = int(self.y - self.radius)

    def draw(self, surface: pygame.Surface):
        """Draw circular golden coin using clean Pygame shapes."""
        center = (int(self.x), int(self.y))

        # 1. Outer Dark Gold Rim
        pygame.draw.circle(surface, self.color_rim, center, self.radius)

        # 2. Main Bright Gold Face
        pygame.draw.circle(surface, self.color_body, center, self.radius - 2)

        # 3. Inner Embossed Relief Ring
        pygame.draw.circle(surface, self.color_inner, center, self.radius - 5, width=1)

        # 4. Center Gold Hub / Symbol
        pygame.draw.circle(surface, self.color_inner, center, 3)

        # 5. Top-Left Shine Highlight
        shine_pos = (int(self.x - 4), int(self.y - 4))
        pygame.draw.circle(surface, self.color_shine, shine_pos, 2)


class CoinManager:
    """Controls coin spawning, road scrolling, boundary cleanup, and player collection."""

    def __init__(self, road_left: int, road_width: int, lane_count: int = 4):
        self.road_left = road_left
        self.road_width = road_width
        self.lane_count = lane_count
        self.lane_width = road_width // lane_count

        self.coins = []
        self.spawn_timer = 1.0  # Initial delay before first coin spawn
        self.spawn_interval = 2.4  # Seconds between spawns

    def reset(self):
        """Clear all active coins and reset spawn timer."""
        self.coins.clear()
        self.spawn_timer = 1.0

    def update(self, dt: float, road_speed: float):
        """
        Update coin positions, trigger timed spawning, and prune off-screen coins.
        :param dt: Frame delta time in seconds
        :param road_speed: Road scrolling speed in px/frame
        """
        road_speed_pps = road_speed * 60.0

        # Spawn timer
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0.0
            self.spawn_coins()

        # Update all active coins
        for coin in self.coins:
            coin.update(dt, road_speed_pps)

        # Remove coins that moved past the bottom of the screen
        self.coins = [c for c in self.coins if c.rect.top < 750]

    def spawn_coins(self):
        """Spawns 1 to 3 coins in a line along a randomly chosen lane."""
        lane_idx = random.randint(0, self.lane_count - 1)
        lane_center_x = self.road_left + (lane_idx * self.lane_width) + (self.lane_width // 2)

        # Spawn a sequence of 1, 2, or 3 coins
        coin_count = random.choice([1, 2, 3])
        start_y = -30.0
        spacing_y = 36.0

        for i in range(coin_count):
            coin_y = start_y - (i * spacing_y)
            self.coins.append(Coin(lane_center_x, coin_y))

    def check_collection(self, player_rect: pygame.Rect) -> int:
        """
        Checks collisions between the player car and active coins.
        Removes collected coins and returns the number of collected coins.
        """
        collected_count = 0
        remaining_coins = []

        for coin in self.coins:
            if player_rect.colliderect(coin.rect):
                collected_count += 1
            else:
                remaining_coins.append(coin)

        self.coins = remaining_coins
        return collected_count

    def draw(self, surface: pygame.Surface):
        """Render all active coins on screen."""
        for coin in self.coins:
            coin.draw(surface)
