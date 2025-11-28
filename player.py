"""Manages Player state."""
from typing import Tuple
from typing_extensions import Self
from dataclasses import dataclass
from character import Character

@dataclass
class Player(Character):
    """Describes the player."""

    def move_to(self, mouse: Tuple[int, int]) -> Self:
        self.x = mouse[0]
        self.y = mouse[1]
        return self

