"""
Indian Traffic Rush — Traffic Module
Member 2: Traffic System

Manages enemy traffic vehicles (Car, Bus, Bike, Auto Rickshaw),
multi-lane intelligent spawning, downward movement, boundary cleanup,
and player-versus-traffic collision detection.
"""

import random
import pygame


class TrafficVehicle:
    """Represents an individual traffic obstacle moving on the road."""

    def __init__(self, vehicle_type: str, x: float, y: float, speed_offset: float, lane_index: int):
        self.vehicle_type = vehicle_type
        self.x = float(x)
        self.y = float(y)
        self.speed_offset = float(speed_offset)  # Relative speed offset (px/s)
        self.lane_index = lane_index

        # Set dimensions and colors based on vehicle type
        if vehicle_type == "bus":
            self.width = 50
            self.height = 120
            self.body_color = random.choice([(185, 28, 28), (29, 78, 216)])  # Red or Blue ST bus
            self.roof_color = (241, 245, 249)
        elif vehicle_type == "auto":
            self.width = 36
            self.height = 62
            self.body_color = (22, 101, 52)     # Green lower body
            self.roof_color = (245, 185, 30)    # Yellow canopy
        elif vehicle_type == "bike":
            self.width = 22
            self.height = 50
            self.body_color = (220, 38, 38)     # Red tank
            self.helmet_color = (249, 115, 22)  # Saffron/orange helmet
        else:  # car
            self.vehicle_type = "car"
            self.width = 42
            self.height = 76
            self.body_color = random.choice([
                (37, 99, 235),   # Blue
                (147, 51, 234),  # Purple
                (51, 65, 85),    # Dark Slate
                (225, 29, 72)    # Crimson
            ])
            self.roof_color = (20, 30, 45)

        # Pygame Rect for position and collision detection
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def update(self, dt: float, road_speed_pps: float, speed_multiplier: float = 1.0):
        """
        Move the vehicle downward relative to the player's forward motion.
        road_speed_pps: Road scrolling speed in pixels per second.
        speed_multiplier: Difficulty speed scaling multiplier.
        """
        downward_speed = road_speed_pps + (self.speed_offset * speed_multiplier)
        self.y += downward_speed * dt
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self, surface: pygame.Surface):
        """Draw vehicle using clean Pygame vector shapes."""
        if self.vehicle_type == "bus":
            self._draw_bus(surface)
        elif self.vehicle_type == "auto":
            self._draw_auto(surface)
        elif self.vehicle_type == "bike":
            self._draw_bike(surface)
        else:
            self._draw_car(surface)

    def _draw_car(self, surface: pygame.Surface):
        # Tires
        pygame.draw.rect(surface, (15, 15, 20), (self.rect.x - 2, self.rect.y + 10, 3, 14), border_radius=2)
        pygame.draw.rect(surface, (15, 15, 20), (self.rect.right - 1, self.rect.y + 10, 3, 14), border_radius=2)
        pygame.draw.rect(surface, (15, 15, 20), (self.rect.x - 2, self.rect.bottom - 24, 3, 14), border_radius=2)
        pygame.draw.rect(surface, (15, 15, 20), (self.rect.right - 1, self.rect.bottom - 24, 3, 14), border_radius=2)

        # Main Body
        pygame.draw.rect(surface, self.body_color, self.rect, border_radius=6)

        # Windshields (Front and Rear)
        front_ws = pygame.Rect(self.rect.x + 5, self.rect.y + 14, self.width - 10, 10)
        pygame.draw.rect(surface, (15, 23, 42), front_ws, border_radius=3)
        rear_ws = pygame.Rect(self.rect.x + 5, self.rect.bottom - 22, self.width - 10, 8)
        pygame.draw.rect(surface, (15, 23, 42), rear_ws, border_radius=2)

        # Roof
        roof_rect = pygame.Rect(self.rect.x + 6, self.rect.y + 26, self.width - 12, 26)
        pygame.draw.rect(surface, self.roof_color, roof_rect, border_radius=2)

        # Taillights
        pygame.draw.rect(surface, (239, 68, 68), (self.rect.x + 3, self.rect.bottom - 3, 6, 2))
        pygame.draw.rect(surface, (239, 68, 68), (self.rect.right - 9, self.rect.bottom - 3, 6, 2))

    def _draw_bus(self, surface: pygame.Surface):
        # 6 Wheels
        tire_color = (15, 15, 20)
        pygame.draw.rect(surface, tire_color, (self.rect.x - 2, self.rect.y + 18, 3, 16))
        pygame.draw.rect(surface, tire_color, (self.rect.right - 1, self.rect.y + 18, 3, 16))
        pygame.draw.rect(surface, tire_color, (self.rect.x - 2, self.rect.bottom - 32, 3, 16))
        pygame.draw.rect(surface, tire_color, (self.rect.right - 1, self.rect.bottom - 32, 3, 16))

        # Main Body
        pygame.draw.rect(surface, self.body_color, self.rect, border_radius=6)

        # White/Silver Roof
        roof_rect = pygame.Rect(self.rect.x + 4, self.rect.y + 16, self.width - 8, self.height - 30)
        pygame.draw.rect(surface, self.roof_color, roof_rect, border_radius=4)

        # Rooftop Luggage Packs
        pygame.draw.rect(surface, (2, 132, 199), (self.rect.x + 8, self.rect.y + 30, 14, 12), border_radius=2)
        pygame.draw.rect(surface, (217, 119, 6), (self.rect.x + 12, self.rect.y + 48, 18, 14), border_radius=2)
        pygame.draw.rect(surface, (5, 150, 105), (self.rect.x + 9, self.rect.y + 68, 16, 12), border_radius=2)

        # Front Windshield & Destination Board
        front_ws = pygame.Rect(self.rect.x + 4, self.rect.y + 4, self.width - 8, 10)
        pygame.draw.rect(surface, (15, 23, 42), front_ws, border_radius=2)
        dest_board = pygame.Rect(self.rect.x + 8, self.rect.y + 2, self.width - 16, 3)
        pygame.draw.rect(surface, (250, 204, 21), dest_board)

        # Rear Taillights
        pygame.draw.rect(surface, (239, 68, 68), (self.rect.x + 2, self.rect.bottom - 4, 8, 3))
        pygame.draw.rect(surface, (239, 68, 68), (self.rect.right - 10, self.rect.bottom - 4, 8, 3))

    def _draw_auto(self, surface: pygame.Surface):
        # Wheels (1 front center, 2 rear)
        pygame.draw.rect(surface, (15, 15, 20), (self.rect.x + self.width // 2 - 2, self.rect.y + 2, 4, 10))
        pygame.draw.rect(surface, (15, 15, 20), (self.rect.x - 2, self.rect.bottom - 16, 3, 12))
        pygame.draw.rect(surface, (15, 15, 20), (self.rect.right - 1, self.rect.bottom - 16, 3, 12))

        # Green Lower Body
        pygame.draw.rect(surface, self.body_color, self.rect, border_radius=6)

        # Yellow Canopy
        canopy_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 12, self.width - 4, self.height - 20)
        pygame.draw.rect(surface, self.roof_color, canopy_rect, border_radius=5)

        # Windshield
        pygame.draw.rect(surface, (15, 23, 42), (self.rect.x + 5, self.rect.y + 8, self.width - 10, 6), border_radius=2)

        # Black Canvas Rear Opening
        rear_canvas = pygame.Rect(self.rect.x + 4, self.rect.bottom - 12, self.width - 8, 6)
        pygame.draw.rect(surface, (30, 41, 59), rear_canvas)

        # Taillights
        pygame.draw.rect(surface, (239, 68, 68), (self.rect.x + 2, self.rect.bottom - 3, 5, 2))
        pygame.draw.rect(surface, (239, 68, 68), (self.rect.right - 7, self.rect.bottom - 3, 5, 2))

    def _draw_bike(self, surface: pygame.Surface):
        # Tires (Front and Rear centerline)
        center_x = self.rect.x + self.width // 2
        pygame.draw.rect(surface, (15, 15, 20), (center_x - 2, self.rect.y + 1, 4, 12))
        pygame.draw.rect(surface, (15, 15, 20), (center_x - 2, self.rect.bottom - 13, 4, 12))

        # Bike Frame / Fuel Tank
        pygame.draw.rect(surface, self.body_color, (center_x - 4, self.rect.y + 12, 8, 12), border_radius=2)

        # Handlebars
        pygame.draw.line(surface, (203, 213, 225), (self.rect.x + 2, self.rect.y + 10), (self.rect.right - 2, self.rect.y + 10), 3)

        # Rider Torso (Dark Jacket)
        pygame.draw.rect(surface, (30, 41, 59), (center_x - 6, self.rect.y + 22, 12, 16), border_radius=3)

        # Rider Helmet
        pygame.draw.circle(surface, self.helmet_color, (center_x, self.rect.y + 18), 5)
        # Helmet Visor
        pygame.draw.rect(surface, (15, 23, 42), (center_x - 4, self.rect.y + 15, 8, 3))

        # Taillight
        pygame.draw.rect(surface, (239, 68, 68), (center_x - 3, self.rect.bottom - 2, 6, 2))


class TrafficManager:
    """Manages multi-lane vehicle spawning, speed progression, and collision detection."""

    def __init__(self, road_left: int, road_width: int, lane_count: int = 4):
        self.road_left = road_left
        self.road_width = road_width
        self.lane_count = lane_count
        self.lane_width = road_width // lane_count

        self.vehicles = []
        self.spawn_timer = 0.5  # Initial quick spawn
        self.base_spawn_interval = 2.0
        self.min_spawn_interval = 0.95

    def reset(self):
        """Clear all active traffic vehicles and reset spawn timer."""
        self.vehicles.clear()
        self.spawn_timer = 0.8

    def update(self, dt: float, road_speed: float, spawn_interval: float = 2.0, speed_multiplier: float = 1.0):
        """
        Update traffic positions, spawn new traffic, and remove off-screen vehicles.
        :param dt: Delta time in seconds
        :param road_speed: Road speed in px/frame (multiplied by 60 for px/s)
        :param spawn_interval: Dynamic spawn interval in seconds based on difficulty
        :param speed_multiplier: Dynamic speed multiplier based on difficulty
        """
        road_speed_pps = road_speed * 60.0

        # Spawn timer progression based on difficulty spawn_interval
        self.spawn_timer += dt
        if self.spawn_timer >= spawn_interval:
            self.spawn_timer = 0.0
            self.spawn_vehicle()

        # Update all active vehicles
        for vehicle in self.vehicles:
            vehicle.update(dt, road_speed_pps, speed_multiplier)

        # Remove vehicles that have moved completely past the bottom of the screen (y > 750)
        self.vehicles = [v for v in self.vehicles if v.rect.top < 750]

    def spawn_vehicle(self, current_score: float = 0.0):
        """Spawns a new traffic vehicle in an available, non-overlapping lane."""
        # Find which lanes are currently clear near the top spawn area (y < 160)
        blocked_lanes = set()
        for v in self.vehicles:
            if v.y < 160:
                blocked_lanes.add(v.lane_index)

        # Safety check: Ensure at least one lane is ALWAYS available to avoid impossible walls
        available_lanes = [l for l in range(self.lane_count) if l not in blocked_lanes]
        if not available_lanes:
            return

        lane_index = random.choice(available_lanes)

        # Weighted random vehicle type selection
        rand_val = random.random()
        if rand_val < 0.35:
            v_type = "car"
            speed_offset = 60.0   # Medium relative downward drift
        elif rand_val < 0.65:
            v_type = "auto"
            speed_offset = 30.0   # Slower
        elif rand_val < 0.82:
            v_type = "bike"
            speed_offset = 110.0  # Faster
        else:
            v_type = "bus"
            speed_offset = 15.0   # Slowest heavy vehicle

        # Slight speed increase at higher scores
        if current_score > 1500:
            speed_offset += random.uniform(5.0, 25.0)

        # Pre-calculate width to center perfectly in lane
        if v_type == "bus":
            width = 50
            height = 120
        elif v_type == "auto":
            width = 36
            height = 62
        elif v_type == "bike":
            width = 22
            height = 50
        else:
            width = 42
            height = 76

        lane_x = self.road_left + (lane_index * self.lane_width)
        x = lane_x + (self.lane_width - width) // 2
        y = -height - random.uniform(20.0, 60.0)

        vehicle = TrafficVehicle(v_type, x, y, speed_offset, lane_index)
        self.vehicles.append(vehicle)

    def check_collision(self, player_rect: pygame.Rect) -> bool:
        """
        Check if the player car's rectangle collides with any traffic vehicle.
        Returns True if a collision occurred.
        """
        for vehicle in self.vehicles:
            if vehicle.rect.colliderect(player_rect):
                return True
        return False

    def draw(self, surface: pygame.Surface):
        """Render all active traffic vehicles."""
        for vehicle in self.vehicles:
            vehicle.draw(surface)
