"""Manages Game state."""
import sys
from dataclasses import dataclass
import pygame

# Get the Python version as a tuple
python_version = sys.version_info

if python_version >= (3, 11):
    # Import for Python 3.11 and above
    from typing import Self
else:
    # Import for Python versions below 3.11
    from typing_extensions import Self


@dataclass
class Game:
    """A game object represents all data necessary to run a game instance."""
    screen: pygame.Surface
    clock: pygame.time.Clock
    background: str
    fps: float
    running: bool
    deltaT: float  # The delta time is change in time in seconds since last frame.


    def tick(self) -> Self:
        """
        Purpose: Limits FPS. Used for framerate-independent physics.
        Examples:
            game.deltaT -> game.clock.tick(game.fps) / 1000
        """
        self.deltaT = self.clock.tick(self.fps) / 1000
        return self
