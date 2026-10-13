"""
Indian Traffic Rush — Music / Audio Module
Stage: Background Music System

Manages background music loading, playback, looping, volume control,
and safe handling of missing audio files or missing audio devices.
"""

import os
import pygame


class MusicManager:
    """Manages background music playback and state synchronization."""

    DEFAULT_MUSIC_PATH = os.path.join("assets", "audio", "background_music.mp3")

    def __init__(self, music_path: str = None, volume: float = 0.4):
        self.music_path = music_path or self.DEFAULT_MUSIC_PATH
        self.volume = max(0.0, min(1.0, volume))
        self.is_available = False
        self.is_loaded = False
        self._warning_printed = False

        self._init_mixer()
        self.load_music(self.music_path)

    def _init_mixer(self):
        """Safely initialize Pygame mixer if not already initialized."""
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.is_available = True
        except Exception as e:
            self.is_available = False
            if not self._warning_printed:
                print(f"[AUDIO WARNING] Pygame mixer initialization failed: {e}")
                print("                Audio playback will be disabled.")
                self._warning_printed = True

    def load_music(self, path: str):
        """Load audio file for background music if available."""
        self.music_path = path
        if not self.is_available:
            return

        if not os.path.isfile(self.music_path):
            if not self._warning_printed:
                print(f"[AUDIO WARNING] Background music file not found at: '{self.music_path}'")
                print("                The game will continue running normally without background music.")
                print("                To add music, place a royalty-free audio file at that location.")
                self._warning_printed = True
            self.is_loaded = False
            return

        try:
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.set_volume(self.volume)
            self.is_loaded = True
        except Exception as e:
            print(f"[AUDIO WARNING] Failed to load audio file '{self.music_path}': {e}")
            self.is_loaded = False

    def play(self, loops: int = -1):
        """
        Start looping background music.
        Does not restart if already actively playing (prevents stuttering or overlapping).
        """
        if not self.is_available or not self.is_loaded:
            return

        try:
            # Only start if not already actively playing
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.music.play(loops=loops)
        except Exception as e:
            print(f"[AUDIO WARNING] Error playing background music: {e}")

    def stop(self):
        """Stop background music if currently playing."""
        if not self.is_available:
            return

        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
        except Exception as e:
            print(f"[AUDIO WARNING] Error stopping background music: {e}")

    def pause(self):
        """Pause background music."""
        if not self.is_available:
            return
        try:
            pygame.mixer.music.pause()
        except Exception:
            pass

    def unpause(self):
        """Unpause background music."""
        if not self.is_available:
            return
        try:
            pygame.mixer.music.unpause()
        except Exception:
            pass

    def set_volume(self, volume: float):
        """Set background music volume (0.0 to 1.0)."""
        self.volume = max(0.0, min(1.0, volume))
        if self.is_available and self.is_loaded:
            try:
                pygame.mixer.music.set_volume(self.volume)
            except Exception:
                pass

    def is_playing(self) -> bool:
        """Returns True if background music is currently playing."""
        if not self.is_available or not self.is_loaded:
            return False
        try:
            return bool(pygame.mixer.music.get_busy())
        except Exception:
            return False
