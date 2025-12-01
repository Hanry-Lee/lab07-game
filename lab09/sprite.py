"""A super-class for anything onscreen that moves."""
import math
from typing import Tuple 
from typing_extensions import Self
from dataclasses import dataclass

@dataclass
class Sprite:
    """A class for anything that is drawn on screen."""
    x: int
    y: int
    size: int

    def direction(self, other: Self) -> Tuple[float, float]:
        vector = (other.x - self.x, other.y - self.y)
        magnitude = math.sqrt(vector[0]**2 + vector[1]**2)
        if magnitude == 0:
            return (0, 0)
        return (vector[0] / magnitude, vector[1] / magnitude)
