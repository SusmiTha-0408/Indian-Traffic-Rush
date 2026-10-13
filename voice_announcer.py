"""
Indian Traffic Rush — Telugu/Telugish Voice Announcer Module
Stage: Voice Announcement System

Manages event-driven Telugu/Telugish voice announcements:
- Level promotions: "Level 2 ra!", "Level 3 ra!", "Level 4 ra!", "Level 5 ra! Super!"
- Police Chase events:
  - Pursuit started: "Police vacchestunnaduroii!"
  - Police close: "Police daggariki vachestundi!"
  - Police danger: "Ayyooo! Police pattukuntundi!"
  - Police caught: "Ayyayyo! Police pattukunnadu!"
- Game Over: "Ayyayyo! Game aipoyindi!"
- Milestone Coins: "Coins super!"
- Nitro boost: "Nitro boost!"

Design & Safety:
- Each event triggers strictly once per occurrence (no spamming/overlapping in game loop).
- Non-blocking and graceful fallback if audio files are missing.
- Background music continues playing undisturbed underneath voice lines.
"""

import os
import pygame


class VoiceAnnouncer:
    """Manages Telugu/Telugish voice sound effect triggers and playback."""

    DEFAULT_VOICE_DIR = os.path.join("assets", "audio", "voice")

    VOICE_FILES = {
        "level_2": "level_2.wav",
        "level_3": "level_3.wav",
        "level_4": "level_4.wav",
        "level_5": "level_5.wav",
        "police_coming": "police_coming.wav",
        "police_close": "police_close.wav",
        "police_danger": "police_danger.wav",
        "police_caught": "police_caught.wav",
        "game_over": "game_over.wav",
        "coins": "coins.wav",
        "nitro": "nitro.wav",
    }

    def __init__(self, voice_dir: str = None, volume: float = 0.85):
        self.voice_dir = voice_dir or self.DEFAULT_VOICE_DIR
        self.volume = max(0.0, min(1.0, volume))
        self.sounds = {}
        self.is_available = False
        self.channel = None

        # Cooldown timer to prevent overlapping voice announcements
        self.cooldown_timer = 0.0
        self.min_interval = 0.8  # Seconds between voice clips

        # Nitro announcement rate-limiter
        self.nitro_cooldown = 0.0

        # State tracking flags to ensure single-trigger announcements
        self.announced_levels = set()
        self.police_active_announced = False
        self.last_police_status = "FAR"
        self.police_caught_announced = False
        self.game_over_announced = False
        self.last_coin_milestone = 0
        self.was_boosting = False

        self._init_audio()
        self.load_sounds()

    def _init_audio(self):
        """Safely ensure mixer is initialized and acquire a dedicated voice channel."""
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.is_available = True
            # Use a high channel index for voice announcements so it won't conflict
            self.channel = pygame.mixer.Channel(7)
        except Exception:
            self.is_available = False
            self.channel = None

    def load_sounds(self):
        """Attempt to load all defined voice files. Missing files are safely skipped."""
        self.sounds.clear()
        if not self.is_available:
            return

        for key, filename in self.VOICE_FILES.items():
            filepath = os.path.join(self.voice_dir, filename)
            if os.path.isfile(filepath):
                try:
                    sound = pygame.mixer.Sound(filepath)
                    sound.set_volume(self.volume)
                    self.sounds[key] = sound
                except Exception:
                    self.sounds[key] = None
            else:
                self.sounds[key] = None

    def update(self, dt: float):
        """Update internal announcement cooldown timers."""
        if self.cooldown_timer > 0.0:
            self.cooldown_timer = max(0.0, self.cooldown_timer - dt)
        if self.nitro_cooldown > 0.0:
            self.nitro_cooldown = max(0.0, self.nitro_cooldown - dt)

    def play(self, sound_key: str) -> bool:
        """
        Play a voice clip by key if loaded, mixer is ready, and cooldown elapsed.
        Returns True if voice clip started playback.
        """
        if not self.is_available:
            return False

        sound = self.sounds.get(sound_key)
        if sound is None:
            return False

        # If a clip is currently playing or cooldown is active, avoid talking over
        if self.cooldown_timer > 0.0:
            return False

        try:
            if self.channel is not None and isinstance(sound, pygame.mixer.Sound):
                self.channel.set_volume(self.volume)
                self.channel.play(sound)
            else:
                sound.play()
            self.cooldown_timer = self.min_interval
            return True
        except Exception:
            return False

    def announce_level(self, level: int) -> bool:
        """
        Announce level crossing ('Level X ra!'). Triggers strictly once per level tier.
        """
        if level <= 1 or level in self.announced_levels:
            return False

        key = f"level_{level}"
        if key in self.VOICE_FILES:
            self.announced_levels.add(level)
            return self.play(key)
        return False

    def announce_police_active(self) -> bool:
        """
        Announce initial Police pursuit ('Police vacchestunnaduroii!').
        Triggers once when chase begins.
        """
        if self.police_active_announced:
            return False

        self.police_active_announced = True
        return self.play("police_coming")

    def announce_police_status(self, current_status: str) -> bool:
        """
        Announce police proximity transitions:
        - Transition into CLOSE ('Police daggariki vachestundi!')
        - Transition into DANGER ('Ayyooo! Police pattukuntundi!')
        Triggers strictly on status transition, never continuously every frame.
        """
        if current_status == self.last_police_status:
            return False

        prev = self.last_police_status
        self.last_police_status = current_status

        if prev == "FAR" and current_status == "CLOSE":
            return self.play("police_close")
        elif current_status == "DANGER" and prev != "DANGER":
            return self.play("police_danger")

        return False

    def announce_police_caught(self) -> bool:
        """
        Announce capture by police ('Ayyayyo! Police pattukunnadu!').
        Triggers strictly once when caught.
        """
        if self.police_caught_announced:
            return False

        self.police_caught_announced = True
        # Force play immediately by resetting cooldown
        self.cooldown_timer = 0.0
        return self.play("police_caught")

    def announce_game_over(self) -> bool:
        """
        Announce normal traffic collision game over ('Ayyayyo! Game aipoyindi!').
        Triggers strictly once on game over.
        """
        if self.game_over_announced:
            return False

        self.game_over_announced = True
        self.cooldown_timer = 0.0
        return self.play("game_over")

    def announce_coins(self, coin_count: int) -> bool:
        """
        Announce coin milestone ('Coins super!') at intervals of 10 coins (10, 20, 30...).
        """
        if coin_count <= 0 or coin_count % 10 != 0:
            return False

        milestone = coin_count // 10
        if milestone <= self.last_coin_milestone:
            return False

        self.last_coin_milestone = milestone
        return self.play("coins")

    def announce_nitro(self, is_boosting: bool) -> bool:
        """
        Announce Nitro engagement ('Nitro boost!') on the rising edge of activation.
        Protected by cooldown so rapid key taps do not spam.
        """
        just_engaged = is_boosting and not self.was_boosting
        self.was_boosting = is_boosting

        if just_engaged and self.nitro_cooldown <= 0.0:
            self.nitro_cooldown = 4.0  # 4-second minimum gap between nitro lines
            return self.play("nitro")

        return False

    def reset(self):
        """
        Reset all announcement flags and timers for a fresh game session.
        Called on start_game, return_to_menu, and restart.
        """
        self.announced_levels.clear()
        self.police_active_announced = False
        self.last_police_status = "FAR"
        self.police_caught_announced = False
        self.game_over_announced = False
        self.last_coin_milestone = 0
        self.was_boosting = False
        self.cooldown_timer = 0.0
        self.nitro_cooldown = 0.0

        if self.channel is not None and self.is_available:
            try:
                self.channel.stop()
            except Exception:
                pass
