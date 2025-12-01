"""A super-class for anything that is trying to win."""
from dataclasses import dataclass
from typing_extensions import Self
from sprite import Sprite

@dataclass
class Character(Sprite):
    """A class for competing entities. Comparable by count (score)."""
    speed: float
    color: str
    count: int = 0

    def __eq__(self, other: object) -> bool:
        """Check if two Characters have the same score."""
        if not isinstance(other, Character):
            return NotImplemented
        return self.count == other.count

    def __lt__(self, other: Self) -> bool:
        """Compare Characters by count/score."""
        return self.count < other.count

    def __le__(self, other: Self) -> bool:
        return self.count <= other.count

    def __gt__(self, other: Self) -> bool:
        return self.count > other.count

    def __ge__(self, other: Self) -> bool:
        return self.count >= other.count

    def eat(self) -> None:
        self.count += 1

    def resize(self) -> None:
        self.size = 10 + self.count
