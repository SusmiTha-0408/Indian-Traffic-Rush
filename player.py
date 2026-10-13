"""
Indian Traffic Rush — Player Module
Member 1: Core / Player

Manages the player's racing car representation, position, keyboard controls,
delta-time based movement, and road boundary clamping.
"""

import pygame


class Player:
    def __init__(self, x: int, y: int, road_left: int, road_right: int):
        """
        Initialize the player racing car.

        :param x: Initial horizontal center/start position
        :param y: Initial vertical position near bottom of the road
        :param road_left: Pixel x-coordinate of the left road edge
        :param road_right: Pixel x-coordinate of the right road edge
        """
        self.width = 44
        self.height = 76
        self.road_left = road_left
        self.road_right = road_right

        # Record starting position for restart/reset
        self.start_x = float(x)
        self.start_y = float(y)
        self.x = float(x)
        self.y = float(y)

        # Movement speed in pixels per second (responsive & controllable)
        self.speed = 320.0

        # Pygame Rect representing collision box and position
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)

        # Visual color palette (Saffron/orange Indian racing livery)
        self.body_color = (235, 95, 25)
        self.stripe_color = (255, 255, 255)
        self.windshield_color = (25, 35, 50)
        self.rear_window_color = (20, 28, 40)
        self.tire_color = (20, 20, 25)
        self.headlight_color = (255, 240, 140)
        self.taillight_color = (220, 38, 38)

    def reset(self):
        """Reset the player car back to its initial starting position."""
        self.x = self.start_x
        self.y = self.start_y
        self.update_rect()

    def update_rect(self):
        """Keep the Pygame Rect synchronized with floating point coordinates."""
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def move_left(self, dt: float = 1.0 / 60.0):
        """
        Move the player car left by speed * dt.
        Clamps to the road left boundary so the car never leaves the road.
        """
        self.x -= self.speed * dt
        if self.x < self.road_left:
            self.x = float(self.road_left)
        self.update_rect()

    def move_right(self, dt: float = 1.0 / 60.0):
        """
        Move the player car right by speed * dt.
        Clamps to the road right boundary so the car never leaves the road.
        """
        max_x = self.road_right - self.width
        self.x += self.speed * dt
        if self.x > max_x:
            self.x = float(max_x)
        self.update_rect()

    def update(self, dt: float = 1.0 / 60.0):
        """
        Update player movement based on keyboard input.
        1. Reads movement input (LEFT / RIGHT arrow keys or A / D).
        2. Calculates movement using frame delta time.
        3. Updates position.
        4. Applies road boundary clamping.
        5. Updates the player Rect.
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.move_left(dt)

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.move_right(dt)

    def draw(self, surface: pygame.Surface):
        """
        Draw the player car on the given Pygame surface.
        Renders saffron body, racing stripes, windshield, tires, and lights.
        """
        # 1. Four Tires (outer edges)
        pygame.draw.rect(surface, self.tire_color, (self.rect.x - 3, self.rect.y + 10, 4, 14), border_radius=2)
        pygame.draw.rect(surface, self.tire_color, (self.rect.right - 1, self.rect.y + 10, 4, 14), border_radius=2)
        pygame.draw.rect(surface, self.tire_color, (self.rect.x - 3, self.rect.bottom - 24, 4, 14), border_radius=2)
        pygame.draw.rect(surface, self.tire_color, (self.rect.right - 1, self.rect.bottom - 24, 4, 14), border_radius=2)

        # 2. Main Saffron/Orange Car Body
        pygame.draw.rect(surface, self.body_color, self.rect, border_radius=8)

        # 3. Dual White Racing Stripes
        stripe_w = 3
        stripe1_x = self.rect.x + (self.width // 2) - 4
        stripe2_x = self.rect.x + (self.width // 2) + 1
        pygame.draw.rect(surface, self.stripe_color, (stripe1_x, self.rect.y + 4, stripe_w, self.height - 8))
        pygame.draw.rect(surface, self.stripe_color, (stripe2_x, self.rect.y + 4, stripe_w, self.height - 8))

        # 4. Front Windshield (aerodynamic trapezoid/rounded)
        windshield_rect = pygame.Rect(self.rect.x + 6, self.rect.y + 16, self.width - 12, 14)
        pygame.draw.rect(surface, self.windshield_color, windshield_rect, border_radius=4)

        # 5. Rear Window
        rear_window_rect = pygame.Rect(self.rect.x + 7, self.rect.bottom - 22, self.width - 14, 10)
        pygame.draw.rect(surface, self.rear_window_color, rear_window_rect, border_radius=3)

        # 6. Front Headlights
        pygame.draw.circle(surface, self.headlight_color, (self.rect.x + 8, self.rect.y + 6), 3)
        pygame.draw.circle(surface, self.headlight_color, (self.rect.right - 8, self.rect.y + 6), 3)

        # 7. Rear Taillights
        pygame.draw.rect(surface, self.taillight_color, (self.rect.x + 6, self.rect.bottom - 4, 6, 2))
        pygame.draw.rect(surface, self.taillight_color, (self.rect.right - 12, self.rect.bottom - 4, 6, 2))
