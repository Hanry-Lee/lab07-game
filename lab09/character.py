"""A super-class for anything that is trying to win."""
from dataclasses import dataclass
from sprite import Sprite

@dataclass
class Character(Sprite):
    """A class for competing entities."""
    speed: float
    color: str
    count: int = 0

    def eat(self) -> None:
        self.count += 1

    def resize(self) -> None:
        self.size = 10 + self.count