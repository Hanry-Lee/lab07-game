"""A super-class for anything onscreen that moves."""
import math
from typing import Tuple
from typing_extensions import Self
from dataclasses import dataclass

@dataclass
class Sprite:
    """A class for anything that is drawn on screen. Comparable by size."""
    x: int
    y: int
    size: int

    def __eq__(self, other: object) -> bool:
        """Check if two Sprites are equal (same position and size)."""
        if not isinstance(other, Sprite):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.size == other.size

    def __lt__(self, other: Self) -> bool:
        """Compare Sprites by size."""
        return self.size < other.size

    def __le__(self, other: Self) -> bool:
        return self.size <= other.size

    def __gt__(self, other: Self) -> bool:
        return self.size > other.size

    def __ge__(self, other: Self) -> bool:
        return self.size >= other.size

    def direction(self, other: Self) -> Tuple[float, float]:
        vector = (other.x - self.x, other.y - self.y)
        magnitude = math.sqrt(vector[0]**2 + vector[1]**2)
        if magnitude == 0:
            return (0, 0)
        return (vector[0] / magnitude, vector[1] / magnitude)
