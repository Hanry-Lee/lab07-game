"""Manages Food state."""
import math
import random
from typing import List, Tuple
from typing_extensions import Self
from dataclasses import dataclass
from sprite import Sprite
from character import Character

@dataclass
class Food(Sprite):
    """Food for the Player to eat."""
    x: float
    y: float
    size: float

    def move(self, dx: int, dy: int) -> Self:
        """
        Purpose: Moves the food by a given amount (dx, dy) in the x and y directions.
        This simulates food drifting or moving slightly within the game world.

        Examples:
            f = Food(x=100, y=100, size=10)
            move(f, 5, -5) -> Food(105, 95, 10)
            move(f, -10, 10) -> Food(95, 105, 10)
        """
        self.x += dx
        self.y += dy
        return self


    def distance(self, spr: Sprite) -> float:
        """
        Purpose: Calculates the Euclidean distance between the food and the player.
        This helps determine proximity for interactions such as eating or collision.

        Examples:
            f = Food(x=100, y=100, size=10)
            p = Player(x=100, y=200, size=10, speed=10, color="red")
            distance(f, p) -> 100.0
        """
        dx = self.x - spr.x
        dy = self.y - spr.y
        return math.sqrt(dx**2 + dy**2)


    def hit(self, spr: Sprite) -> bool:
        """
        Purpose: Determines whether a Player and Food are touching
        Examples:
            f = Food(x=0, y=0, size=1)
            p1 = Player(x=0, y=10, size=10, speed=10, "red")
            p2 = Player(x=0, y=11, size=10, speed=10, "red")
            f.hit(p1) -> True
            f.hit(p2) -> False
        """
        if self.distance(spr) < self.size + spr.size:
            return True
        return False

@dataclass
class FoodList:
    """A containing class for Food."""
    food: List[Food]


    def populate(self, amount: int, bounds: Tuple[int, int]) -> List[Food]:
        """
        Purpose: Populates the game world with a specified amount of food, placing them
        randomly within the given bounds (width and height). This initializes a list of
        food items to be consumed by players.

        Examples:
            food_list = FoodList([])
            populate(food_list, 5, (500, 500)) -> List of 5 food objects within the 500x500 bounds
        """
        for i in range(amount):
            self.food.append(
                Food(
                    x=random.randint(0, bounds[0]),
                    y=random.randint(0, bounds[1]),
                    size=10
                )
            )
        return self.food


    def eat(self, chr: Character) -> List[Food]:
        """
        Purpose: Checks if the player is hitting any food in the list. If so, the food is removed,
        and the player's food consumption count increases. The player is then resized accordingly.

        Examples:
            food_list = FoodList([Food(x=0, y=0, size=10)])
            p = Player(x=0, y=0, size=10, speed=10, color="red")
            eat(food_list, p) -> Removes the food and increases player count.
        """
        for f in self.food:
            if f.hit(chr):
                chr.eat()
                chr.resize()
                self.food.remove(f)
        return self.food


    def move(self, bounds: Tuple[int, int] = (1280, 720)) -> Self:
        """
        Purpose: Randomly moves all the food items in the list by a small amount. This simulates
        the movement of food drifting around the game world.

        Examples:
            food_list = FoodList([Food(x=100, y=100, size=10)])
            move(food_list) -> Moves all food items slightly by random amounts.
        """
        for f in self.food:
            f.move(random.randint(-1, 1), random.randint(-1, 1))
            f.x = max(f.size, min(bounds[0] - f.size, f.x))
            f.y = max(f.size, min(bounds[1] - f.size, f.y))
        return self
