"""
Indian Traffic Rush — Police Chase Module
Stage 10: Police Chase System

Manages the police interceptor vehicle:
- Position & road boundary clamping
- Activation at Difficulty Level >= 3 (Score >= 500)
- Delta-time catch-up physics & lateral tracking
- Nitro interaction (player pulls away / police falls behind)
- Difficulty-based catch-up speed scaling
- Catch distance & Game Over trigger
- Procedural Pygame vector drawing with flashing emergency siren light bar
"""

import pygame


class PoliceChase:
    """Manages the police chase vehicle and pursuit dynamics."""

    def __init__(self, road_left: int, road_right: int):
        self.road_left = road_left
        self.road_right = road_right

        # Vehicle Dimensions
        self.width = 44
        self.height = 76

        # State
        self.active = False
        self.caught = False

        # Position (Internal coordinates)
        self._x = float(road_left + 100)
        self._y = 800.0  # Spawn off-screen bottom initially

        # Pygame Rect representing collision box and position
        self.rect = pygame.Rect(int(self._x), int(self._y), self.width, self.height)

        # Movement & Catch-up Speeds
        self.base_speed = 300.0          # Base forward speed (px/s)
        self.catch_up_speed = 35.0       # Base relative catch-up speed toward player (px/s)
        self.steer_speed = 220.0         # Lateral steering tracking speed (px/s)
        self.fall_back_speed = 55.0      # Speed at which police falls behind when player uses Nitro (px/s)

        # Distance & Catch Thresholds
        self.minimum_distance = 25.0     # Visual proximity threshold (px)
        self.catch_distance = 10.0       # Catch distance triggering Game Over (px)
        self.distance = 150.0            # Current distance from player rear to police front (px)
        self.distance_status = "FAR"     # "FAR", "CLOSE", "DANGER"

        # Notification & Siren
        self.notification_timer = 0.0
        self.notification_text = "POLICE CHASE!"
        self.strobe_timer = 0.0
        self.strobe_state = 0            # 0: Red Left / 1: Blue Right

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, val: float):
        self._x = float(val)
        self.rect.x = int(self._x)

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, val: float):
        self._y = float(val)
        self.rect.y = int(self._y)

    @property
    def police_x(self) -> float:
        return self._x

    @police_x.setter
    def police_x(self, val: float):
        self._x = float(val)
        self.rect.x = int(self._x)

    @property
    def police_y(self) -> float:
        return self._y

    @police_y.setter
    def police_y(self, val: float):
        self._y = float(val)
        self.rect.y = int(self._y)

    def activate(self, player_x: float = 240.0, player_y: float = 550.0):
        """
        Activate the police chase. Spawns behind the player's vehicle.
        """
        self.active = True
        self.caught = False

        # Align with player horizontally, clamped within road boundaries
        self.x = float(player_x)
        max_x = float(self.road_right - self.width)
        self.x = max(float(self.road_left), min(max_x, self.x))

        # Position behind player (spawn ~130px behind player bottom)
        player_bottom = player_y + 76.0
        self.y = player_bottom + 130.0

        self.distance = self.y - player_bottom
        self.distance_status = "FAR"
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # Visual notification banner
        self.notification_timer = 1.5
        self.notification_text = "POLICE CHASE!"
        self.strobe_timer = 0.0
        self.strobe_state = 0

    def reset(self):
        """Reset the police chase system back to initial inactive state."""
        self.active = False
        self.caught = False
        self.x = float(self.road_left + 100)
        self.y = 800.0
        self.distance = 200.0
        self.distance_status = "FAR"
        self.notification_timer = 0.0
        self.strobe_timer = 0.0
        self.strobe_state = 0
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def update(
        self,
        dt: float,
        player_rect: pygame.Rect = None,
        is_boosting: bool = False,
        catch_up_multiplier: float = 1.0,
        road_speed: float = 5.0
    ):
        """
        Update police movement, lateral steering, catch-up distance, and siren timer.
        """
        if not self.active:
            return

        # 1. Update notification timer
        if self.notification_timer > 0.0:
            self.notification_timer = max(0.0, self.notification_timer - dt)

        # 2. Update alternating siren strobe timer
        self.strobe_timer += dt
        if self.strobe_timer >= 0.12:
            self.strobe_timer = 0.0
            self.strobe_state = 1 - self.strobe_state

        if player_rect is None:
            return

        # 3. Horizontal (X) tracking toward player
        target_x = float(player_rect.x)
        dx = target_x - self.x
        if abs(dx) > 1.0:
            step = self.steer_speed * dt
            if abs(dx) <= step:
                self.x = target_x
            else:
                self.x += step if dx > 0 else -step

        # Clamp X inside road boundaries
        max_x = float(self.road_right - self.width)
        self.x = max(float(self.road_left), min(max_x, self.x))

        # 4. Vertical (Y) catch-up / fall-back physics
        current_gap = self.y - player_rect.bottom
        self.distance = current_gap

        if is_boosting:
            # Player is accelerating with Nitro -> Police falls behind
            self.y += self.fall_back_speed * dt
            # Clamp maximum backward distance so police doesn't fall off forever
            max_gap = 210.0
            if self.y > player_rect.bottom + max_gap:
                self.y = player_rect.bottom + max_gap
        else:
            # Normal speed -> Police gradually catches up
            effective_catch_up = self.catch_up_speed * catch_up_multiplier

            if current_gap > 80.0:
                # Far behind: faster catch-up
                gap_factor = min(2.0, 1.0 + (current_gap - 80.0) / 100.0)
                rel_speed = effective_catch_up * gap_factor
            else:
                # Close proximity: careful approach
                gap_factor = max(0.6, current_gap / 80.0)
                rel_speed = effective_catch_up * gap_factor

            self.y -= rel_speed * dt

        # Update rect and distance
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.distance = self.y - player_rect.bottom

        # 5. Update distance status indicator
        if self.distance > 100.0:
            self.distance_status = "FAR"
        elif self.distance > 45.0:
            self.distance_status = "CLOSE"
        else:
            self.distance_status = "DANGER"

    def check_catch(self, player_rect: pygame.Rect) -> bool:
        """
        Check if the police vehicle has caught the player.
        Returns True if police reached catch distance or rect collided.
        """
        if not self.active:
            return False

        # 1. Direct bounding box collision
        if self.rect.colliderect(player_rect):
            self.caught = True
            return True

        # 2. Catch distance threshold with lateral alignment
        gap = self.y - player_rect.bottom
        if gap <= self.catch_distance:
            lateral_gap = abs(self.rect.centerx - player_rect.centerx)
            if lateral_gap < (self.width + player_rect.width) * 0.5:
                self.caught = True
                return True

        return False

    def get_distance_status(self, player_rect: pygame.Rect = None) -> str:
        """Return 'FAR', 'CLOSE', or 'DANGER' based on distance to player."""
        if not self.active:
            return ""
        if player_rect is not None:
            dist = self.y - player_rect.bottom
        else:
            dist = self.distance

        if dist > 100.0:
            return "FAR"
        elif dist > 45.0:
            return "CLOSE"
        else:
            return "DANGER"

    def draw(self, surface: pygame.Surface):
        """
        Procedurally render the Indian Police Cruiser using Pygame vector shapes:
        - Dark cruiser body
        - Dual white door/side panels
        - White roof
        - Front windshield and rear window
        - Dual front headlights & red taillights
        - Push bumper (bull-bar)
        - Roof emergency siren light bar with alternating flashing red/blue strobes
        """
        if not self.active:
            return

        x = self.rect.x
        y = self.rect.y
        w = self.width
        h = self.height

        # 1. Wheels / Tires (outer edges)
        tire_color = (15, 15, 20)
        pygame.draw.rect(surface, tire_color, (x - 3, y + 10, 4, 14), border_radius=2)
        pygame.draw.rect(surface, tire_color, (x + w - 1, y + 10, 4, 14), border_radius=2)
        pygame.draw.rect(surface, tire_color, (x - 3, y + h - 24, 4, 14), border_radius=2)
        pygame.draw.rect(surface, tire_color, (x + w - 1, y + h - 24, 4, 14), border_radius=2)

        # 2. Main Police Cruiser Body (Dark Navy / Black)
        body_color = (18, 24, 38)
        pygame.draw.rect(surface, body_color, self.rect, border_radius=8)

        # 3. White Door Side Panels
        white_panel = (248, 250, 252)
        panel_w = 4
        pygame.draw.rect(surface, white_panel, (x + 2, y + 22, panel_w, 32), border_radius=1)
        pygame.draw.rect(surface, white_panel, (x + w - 6, y + 22, panel_w, 32), border_radius=1)

        # 4. Front Push Bumper (Bull Bar)
        pygame.draw.rect(surface, (71, 85, 105), (x + 8, y - 2, w - 16, 4), border_radius=2)

        # 5. Front Windshield (curved trapezoid)
        front_ws = pygame.Rect(x + 6, y + 16, w - 12, 12)
        pygame.draw.rect(surface, (30, 41, 59), front_ws, border_radius=3)

        # 6. Rear Window
        rear_ws = pygame.Rect(x + 7, y + h - 22, w - 14, 10)
        pygame.draw.rect(surface, (30, 41, 59), rear_ws, border_radius=3)

        # 7. White Roof Panel
        roof_rect = pygame.Rect(x + 7, y + 28, w - 14, 24)
        pygame.draw.rect(surface, (241, 245, 249), roof_rect, border_radius=3)

        # 8. Front Headlights (Bright Yellow-White)
        pygame.draw.circle(surface, (255, 250, 180), (x + 8, y + 5), 3)
        pygame.draw.circle(surface, (255, 250, 180), (x + w - 8, y + 5), 3)

        # 9. Rear Taillights
        pygame.draw.rect(surface, (220, 38, 38), (x + 5, y + h - 3, 6, 2))
        pygame.draw.rect(surface, (220, 38, 38), (x + w - 11, y + h - 3, 6, 2))

        # 10. Emergency Siren Light Bar (Center Roof)
        bar_w = 26
        bar_h = 7
        bar_x = x + (w - bar_w) // 2
        bar_y = y + 36
        pygame.draw.rect(surface, (30, 41, 59), (bar_x - 1, bar_y - 1, bar_w + 2, bar_h + 2), border_radius=2)

        # Alternating Red/Blue strobes with glow
        if self.strobe_state == 0:
            red_color = (255, 40, 40)
            blue_color = (30, 60, 160)
            glow_surf = pygame.Surface((18, 18), pygame.SRCALPHA)
            glow_surf.fill((255, 40, 40, 60))
            surface.blit(glow_surf, (bar_x - 4, bar_y - 5))
        else:
            red_color = (160, 30, 30)
            blue_color = (50, 150, 255)
            glow_surf = pygame.Surface((18, 18), pygame.SRCALPHA)
            glow_surf.fill((50, 150, 255, 60))
            surface.blit(glow_surf, (bar_x + bar_w // 2 - 2, bar_y - 5))

        # Left half: Red strobe
        pygame.draw.rect(surface, red_color, (bar_x, bar_y, bar_w // 2, bar_h), border_radius=2)
        # Right half: Blue strobe
        pygame.draw.rect(surface, blue_color, (bar_x + bar_w // 2, bar_y, bar_w // 2, bar_h), border_radius=2)
