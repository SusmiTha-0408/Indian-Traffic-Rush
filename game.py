"""
Indian Traffic Rush — Game Controller
Member 1: Core / Player

Coordinates the game loop, game states, road scrolling,
and connects player, traffic, coins, nitro, and UI modules.
"""

import sys
import pygame

from player import Player
from traffic import TrafficManager
from coins import CoinManager
from nitro import NitroSystem
from difficulty import DifficultyManager
from police import PoliceChase
from audio import MusicManager
from voice_announcer import VoiceAnnouncer
from ui import UI

# ========================================================
# CONFIGURATION CONSTANTS
# ========================================================
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
FPS = 60

ROAD_LEFT = 60
ROAD_WIDTH = 380
ROAD_RIGHT = ROAD_LEFT + ROAD_WIDTH
LANE_COUNT = 4
LANE_WIDTH = ROAD_WIDTH // LANE_COUNT

BASE_ROAD_SPEED = 5.0

COLOR_GRASS = (22, 101, 52)
COLOR_ASPHALT = (30, 36, 48)
COLOR_LANE_WHITE = (248, 250, 252)
COLOR_LANE_YELLOW = (250, 204, 21)
COLOR_RUMBLE_RED = (220, 38, 38)
COLOR_RUMBLE_WHITE = (248, 250, 252)


class Game:
    def __init__(self):
        # 1. Pygame Initialization
        pygame.init()
        pygame.display.set_caption("Indian Traffic Rush — Prototype")

        # 2. Window and Clock
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.is_running = True

        # 3. Game States: "MENU", "PLAYING", "GAME_OVER"
        self.state = "MENU"

        # 4. Road Scrolling Parameters
        self.road_speed = BASE_ROAD_SPEED
        self.dash_length = 36
        self.dash_gap = 30
        self.dash_total = self.dash_length + self.dash_gap
        self.road_offset = 0.0

        # 5. Modular Subsystems
        player_start_x = ROAD_LEFT + (ROAD_WIDTH // 2) - 22
        player_start_y = SCREEN_HEIGHT - 120
        self.player = Player(player_start_x, player_start_y, ROAD_LEFT, ROAD_RIGHT)
        self.traffic = TrafficManager(ROAD_LEFT, ROAD_WIDTH, LANE_COUNT)
        self.coins = CoinManager(ROAD_LEFT, ROAD_WIDTH, LANE_COUNT)
        self.nitro = NitroSystem()
        self.difficulty = DifficultyManager()
        self.police = PoliceChase(ROAD_LEFT, ROAD_RIGHT)
        self.music = MusicManager()
        self.voice = VoiceAnnouncer()
        self.ui = UI(SCREEN_WIDTH, SCREEN_HEIGHT)

        # 6. Score and Economy
        self.score = 0.0
        self.coin_count = 0
        self.caught_by_police = False
        self.space_consumed = False

    def start_game(self):
        """Transition from Menu or Game Over to Playing state with a completely fresh session."""
        self.state = "PLAYING"
        self.score = 0.0
        self.coin_count = 0
        self.caught_by_police = False
        self.space_consumed = True
        self.road_speed = BASE_ROAD_SPEED
        self.road_offset = 0.0
        self.player.reset()
        self.traffic.reset()
        self.coins.reset()
        self.nitro.reset()
        self.difficulty.reset()
        self.police.reset()
        self.music.play()
        self.voice.reset()

    def return_to_menu(self):
        """Return to MENU state and reset gameplay systems."""
        self.state = "MENU"
        self.caught_by_police = False
        self.space_consumed = False
        self.road_speed = BASE_ROAD_SPEED
        self.road_offset = 0.0
        self.player.reset()
        self.traffic.reset()
        self.coins.reset()
        self.nitro.reset()
        self.difficulty.reset()
        self.police.reset()
        self.music.stop()
        self.voice.reset()

    def run(self):
        """Main game loop running at target 60 FPS."""
        while self.is_running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            dt = min(dt, 0.1)  # Guard against frame lag spikes draining Nitro excessively

            self.handle_events()
            self.update(dt)
            self.draw()

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def handle_events(self):
        """Process player input and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            elif event.type == pygame.KEYDOWN:
                if self.state == "MENU":
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.is_running = False

                elif self.state == "PLAYING":
                    if event.key == pygame.K_ESCAPE:
                        self.return_to_menu()

                elif self.state == "GAME_OVER":
                    if event.key == pygame.K_r:
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.return_to_menu()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.space_consumed = False

    def update(self, dt: float):
        """Update game state and active entities."""
        if self.state != "PLAYING":
            self.nitro.is_active = False
            self.music.stop()
            return

        # 0. Update voice announcement cooldown timers
        self.voice.update(dt)

        # 1. Update difficulty based on current score
        self.difficulty.update(self.score, dt)
        diff_multiplier = self.difficulty.current_multiplier
        spawn_interval = self.difficulty.current_spawn_interval

        # Voice: Level promotion announcement (triggers strictly once per level tier)
        self.voice.announce_level(self.difficulty.current_level)

        # 2. Read Nitro input (SPACE key physically held down during PLAYING)
        keys = pygame.key.get_pressed()
        if not keys[pygame.K_SPACE]:
            self.space_consumed = False

        is_space_held = bool(keys[pygame.K_SPACE]) and not self.space_consumed

        # 3. Update Nitro system & calculate effective road speed:
        # BASE SPEED -> DIFFICULTY MULTIPLIER -> NITRO MULTIPLIER -> EFFECTIVE ROAD SPEED
        self.nitro.update(is_space_held, dt)
        effective_road_speed = BASE_ROAD_SPEED * diff_multiplier * self.nitro.get_multiplier()
        self.road_speed = effective_road_speed

        # Voice: Nitro boost announcement (rising edge activation, cooldown guarded)
        self.voice.announce_nitro(self.nitro.is_active)

        # 4. Update road scroll offset
        self.road_offset = (self.road_offset + self.road_speed) % self.dash_total

        # 5. Update player (input reading, delta-time movement & boundary clamping)
        self.player.update(dt)

        # 6. Update score (+10 per second)
        self.score += 10.0 * dt

        # 7. Update traffic and coins with effective road speed and difficulty parameters
        self.traffic.update(dt, self.road_speed, spawn_interval, diff_multiplier)
        self.coins.update(dt, self.road_speed)

        # 8. Coin collection check (1 coin = +10 score)
        collected_coins = self.coins.check_collection(self.player.rect)
        if collected_coins > 0:
            self.coin_count += collected_coins
            self.score += collected_coins * 10.0
            # Voice: Coin collection milestone announcement (every 10 coins)
            self.voice.announce_coins(self.coin_count)

        # 9. Collision detection (Player vs Traffic)
        if self.traffic.check_collision(self.player.rect):
            self.state = "GAME_OVER"
            self.caught_by_police = False
            self.nitro.is_active = False
            self.music.stop()
            # Voice: Normal traffic collision game over announcement
            self.voice.announce_game_over()
            return

        # 10. Police Chase System
        # Activates at Difficulty Level >= 3 (Score >= 500)
        if self.difficulty.current_level >= 3:
            if not self.police.active:
                self.police.activate(self.player.x, self.player.y)
                # Voice: Police pursuit started announcement
                self.voice.announce_police_active()
        else:
            if self.police.active:
                self.police.reset()

        if self.police.active:
            # Difficulty catch-up scaling: L3 -> 1.0, L4 -> 1.1, L5 -> 1.2
            p_mult = 1.0
            if self.difficulty.current_level == 4:
                p_mult = 1.1
            elif self.difficulty.current_level >= 5:
                p_mult = 1.2

            self.police.update(
                dt=dt,
                player_rect=self.player.rect,
                is_boosting=self.nitro.is_active,
                catch_up_multiplier=p_mult,
                road_speed=self.road_speed
            )

            # Voice: Police proximity status transition (FAR -> CLOSE, CLOSE -> DANGER)
            self.voice.announce_police_status(self.police.distance_status)

            # Check police catch condition
            if self.police.check_catch(self.player.rect):
                self.state = "GAME_OVER"
                self.caught_by_police = True
                self.nitro.is_active = False
                self.music.stop()
                # Voice: Caught by police announcement
                self.voice.announce_police_caught()

    def draw(self):
        """Render the complete game frame."""
        # Draw road environment
        self.draw_road()

        if self.state == "PLAYING":
            # Draw game entities
            self.coins.draw(self.screen)
            self.traffic.draw(self.screen)
            if self.police.active:
                self.police.draw(self.screen)
            self.nitro.draw_effects(self.screen, self.player.rect)
            self.player.draw(self.screen)

            # Draw HUD with Level indicator, transition notification, and Police Chase HUD
            self.ui.draw_hud(
                self.screen,
                self.score,
                self.coin_count,
                self.nitro.get_percentage(),
                self.difficulty.current_level,
                self.difficulty.banner_text,
                self.difficulty.banner_timer,
                self.police.active,
                self.police.distance_status,
                self.police.notification_timer,
                self.police.notification_text
            )

        elif self.state == "MENU":
            # Draw player parked on highway under the menu
            self.player.draw(self.screen)
            self.ui.draw_menu(self.screen)

        elif self.state == "GAME_OVER":
            # Draw frozen coins, traffic, police and player under the game over overlay
            self.coins.draw(self.screen)
            self.traffic.draw(self.screen)
            if self.police.active:
                self.police.draw(self.screen)
            self.player.draw(self.screen)
            self.ui.draw_game_over(self.screen, self.score, self.coin_count, self.caught_by_police)

    def draw_road(self):
        """Draw the moving highway, shoulders, and lane dividers."""
        # 1. Roadside Grass Shoulders
        self.screen.fill(COLOR_GRASS)

        # 2. Asphalt Highway Surface
        road_rect = pygame.Rect(ROAD_LEFT, 0, ROAD_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, COLOR_ASPHALT, road_rect)

        # 3. Red and White Shoulder Rumble Strips
        rumble_width = 8
        rumble_h = 24
        rumble_offset = int(self.road_offset) % (rumble_h * 2)

        for y in range(-rumble_h * 2 + rumble_offset, SCREEN_HEIGHT + rumble_h, rumble_h):
            color = COLOR_RUMBLE_RED if ((y // rumble_h) % 2 == 0) else COLOR_RUMBLE_WHITE
            # Left rumble
            pygame.draw.rect(self.screen, color, (ROAD_LEFT - rumble_width, y, rumble_width, rumble_h))
            # Right rumble
            pygame.draw.rect(self.screen, color, (ROAD_RIGHT, y, rumble_width, rumble_h))

        # 4. Solid White Road Edge Boundaries
        pygame.draw.line(self.screen, COLOR_LANE_WHITE, (ROAD_LEFT + 2, 0), (ROAD_LEFT + 2, SCREEN_HEIGHT), 2)
        pygame.draw.line(self.screen, COLOR_LANE_WHITE, (ROAD_RIGHT - 2, 0), (ROAD_RIGHT - 2, SCREEN_HEIGHT), 2)

        # 5. Moving Dashed Lane Dividers
        for lane_idx in range(1, LANE_COUNT):
            lane_x = ROAD_LEFT + (lane_idx * LANE_WIDTH)
            # Center divider has amber line
            dash_color = COLOR_LANE_YELLOW if lane_idx == 2 else COLOR_LANE_WHITE

            for y in range(int(self.road_offset) - self.dash_total, SCREEN_HEIGHT + self.dash_total, self.dash_total):
                pygame.draw.line(self.screen, dash_color, (lane_x, y), (lane_x, y + self.dash_length), 3)
