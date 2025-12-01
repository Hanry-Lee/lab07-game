"""Manages Food state."""
import math
import random
from functools import reduce
from typing import List, Tuple, Callable, Optional, Iterator
from typing_extensions import Self
from dataclasses import dataclass
from sprite import Sprite
from character import Character

@dataclass
class Food(Sprite):
    """Food for the Player to eat. Comparable by size."""
    x: float
    y: float
    size: float

    def __add__(self, other: "Food") -> "Food":
        """Add two foods together (combine positions and sizes)."""
        return Food(x=self.x + other.x, y=self.y + other.y, size=self.size + other.size)

    def __sub__(self, other: "Food") -> "Food":
        """Subtract one food from another."""
        return Food(x=self.x - other.x, y=self.y - other.y, size=abs(self.size - other.size))

    def __mul__(self, scalar: float) -> "Food":
        """Scale a food's position and size."""
        return Food(x=self.x * scalar, y=self.y * scalar, size=self.size * scalar)

    def __eq__(self, other: object) -> bool:
        """Check if two foods are equal."""
        if not isinstance(other, Food):
            return False
        return self.x == other.x and self.y == other.y and self.size == other.size

    def __lt__(self, other: "Food") -> bool:
        """Compare foods by size."""
        return self.size < other.size

    def __le__(self, other: "Food") -> bool:
        return self.size <= other.size

    def __gt__(self, other: "Food") -> bool:
        return self.size > other.size

    def __ge__(self, other: "Food") -> bool:
        return self.size >= other.size

    def is_in_bounds(self, bounds: Tuple[int, int]) -> bool:
        """Check if food is within the given bounds."""
        return 0 <= self.x <= bounds[0] and 0 <= self.y <= bounds[1]

    def is_near(self, point: Tuple[float, float], radius: float) -> bool:
        """Check if food is within radius of a point."""
        dist = math.sqrt((self.x - point[0])**2 + (self.y - point[1])**2)
        return dist <= radius

    def move(self, dx: int, dy: int) -> Self:
        """Move the food by (dx, dy)."""
        self.x += dx
        self.y += dy
        return self

    def distance(self, spr: Sprite) -> float:
        """Calculate distance to another sprite."""
        dx = self.x - spr.x
        dy = self.y - spr.y
        return math.sqrt(dx**2 + dy**2)

    def hit(self, spr: Sprite) -> bool:
        """Check if this food is touching the sprite."""
        return self.distance(spr) < self.size + spr.size


@dataclass
class FoodList:
    """A container class for Food with map/filter/reduce/sort operations."""
    food: List[Food]

    def __iter__(self) -> Iterator[Food]:
        return iter(self.food)

    def __len__(self) -> int:
        return len(self.food)

    def __getitem__(self, index: int) -> Food:
        return self.food[index]

    def __contains__(self, item: Food) -> bool:
        return item in self.food

    def __add__(self, other: "FoodList") -> "FoodList":
        """Combine two food lists."""
        return FoodList(self.food + other.food)

    def __sub__(self, other: "FoodList") -> "FoodList":
        """Remove foods in other from self."""
        return FoodList([f for f in self.food if f not in other.food])

    def add(self, food_item: Food) -> Self:
        """Add a food item to the list."""
        self.food.append(food_item)
        return self

    def remove(self, food_item: Food) -> Self:
        """Remove a food item from the list."""
        if food_item in self.food:
            self.food.remove(food_item)
        return self

    def map(self, func: Callable[[Food], Food]) -> "FoodList":
        """Apply a function to each food."""
        return FoodList(list(map(func, self.food)))

    def grow_all(self, amount: float) -> "FoodList":
        """Increase size of all food by amount."""
        return self.map(lambda f: Food(f.x, f.y, f.size + amount))

    def shrink_all(self, amount: float) -> "FoodList":
        """Decrease size of all food by amount."""
        return self.map(lambda f: Food(f.x, f.y, max(1, f.size - amount)))

    def scale_all(self, factor: float) -> "FoodList":
        """Scale all food sizes by a factor."""
        return self.map(lambda f: f * factor)

    def move_all(self, dx: float, dy: float) -> "FoodList":
        """Move all food by (dx, dy)."""
        return self.map(lambda f: Food(f.x + dx, f.y + dy, f.size))

    def filter(self, predicate: Callable[[Food], bool]) -> "FoodList":
        """Keep only foods that satisfy the predicate."""
        return FoodList(list(filter(predicate, self.food)))

    def filter_by_size(self, min_size: float, max_size: float) -> "FoodList":
        """Keep only foods within size range."""
        return self.filter(lambda f: min_size <= f.size <= max_size)

    def filter_in_bounds(self, bounds: Tuple[int, int]) -> "FoodList":
        """Keep only foods within bounds."""
        return self.filter(lambda f: f.is_in_bounds(bounds))

    def filter_near(self, point: Tuple[float, float], radius: float) -> "FoodList":
        """Keep only foods within radius of point."""
        return self.filter(lambda f: f.is_near(point, radius))

    def filter_hittable_by(self, spr: Sprite) -> "FoodList":
        """Keep only foods that can be hit by the sprite."""
        return self.filter(lambda f: f.hit(spr))

    def sort(self, reverse: bool = False) -> "FoodList":
        """Return a new FoodList sorted by size."""
        return FoodList(sorted(self.food, reverse=reverse))

    def sort_by_size(self, reverse: bool = False) -> "FoodList":
        """Sort foods by size."""
        return FoodList(sorted(self.food, key=lambda f: f.size, reverse=reverse))

    def sort_by_distance(self, point: Tuple[float, float], reverse: bool = False) -> "FoodList":
        """Sort foods by distance from a point."""
        def dist(f: Food) -> float:
            return math.sqrt((f.x - point[0])**2 + (f.y - point[1])**2)
        return FoodList(sorted(self.food, key=dist, reverse=reverse))

    def sort_by_x(self, reverse: bool = False) -> "FoodList":
        """Sort foods by x position."""
        return FoodList(sorted(self.food, key=lambda f: f.x, reverse=reverse))

    def sort_by_y(self, reverse: bool = False) -> "FoodList":
        """Sort foods by y position."""
        return FoodList(sorted(self.food, key=lambda f: f.y, reverse=reverse))

    def reduce(self, func: Callable[[Food, Food], Food], initial: Optional[Food] = None) -> Optional[Food]:
        """Reduce the food list to a single Food."""
        if not self.food:
            return initial
        if initial is not None:
            return reduce(func, self.food, initial)
        return reduce(func, self.food)

    def total_size(self) -> float:
        """Sum of all food sizes."""
        if not self.food:
            return 0.0
        return reduce(lambda acc, f: acc + f.size, self.food, 0.0)

    def average_size(self) -> float:
        """Average size of all foods."""
        if not self.food:
            return 0.0
        return self.total_size() / len(self.food)

    def center_of_mass(self) -> Tuple[float, float]:
        """Calculate average position of all foods."""
        if not self.food:
            return (0.0, 0.0)
        total_x = reduce(lambda acc, f: acc + f.x, self.food, 0.0)
        total_y = reduce(lambda acc, f: acc + f.y, self.food, 0.0)
        n = len(self.food)
        return (total_x / n, total_y / n)

    def largest(self) -> Optional[Food]:
        """Find the largest food."""
        if not self.food:
            return None
        return reduce(lambda a, b: a if a.size >= b.size else b, self.food)

    def smallest(self) -> Optional[Food]:
        """Find the smallest food."""
        if not self.food:
            return None
        return reduce(lambda a, b: a if a.size <= b.size else b, self.food)

    def closest_to(self, point: Tuple[float, float]) -> Optional[Food]:
        """Find food closest to a point."""
        if not self.food:
            return None
        def closer(a: Food, b: Food) -> Food:
            dist_a = math.sqrt((a.x - point[0])**2 + (a.y - point[1])**2)
            dist_b = math.sqrt((b.x - point[0])**2 + (b.y - point[1])**2)
            return a if dist_a <= dist_b else b
        return reduce(closer, self.food)

    def farthest_from(self, point: Tuple[float, float]) -> Optional[Food]:
        """Find food farthest from a point."""
        if not self.food:
            return None
        def farther(a: Food, b: Food) -> Food:
            dist_a = math.sqrt((a.x - point[0])**2 + (a.y - point[1])**2)
            dist_b = math.sqrt((b.x - point[0])**2 + (b.y - point[1])**2)
            return a if dist_a >= dist_b else b
        return reduce(farther, self.food)

    def any_in_bounds(self, bounds: Tuple[int, int]) -> bool:
        """Check if any food is within bounds."""
        return any(f.is_in_bounds(bounds) for f in self.food)

    def all_in_bounds(self, bounds: Tuple[int, int]) -> bool:
        """Check if all foods are within bounds."""
        return all(f.is_in_bounds(bounds) for f in self.food)

    def any_near(self, point: Tuple[float, float], radius: float) -> bool:
        """Check if any food is within radius of point."""
        return any(f.is_near(point, radius) for f in self.food)

    def is_empty(self) -> bool:
        """Check if the food list is empty."""
        return len(self.food) == 0

    def populate(self, amount: int, bounds: Tuple[int, int]) -> List[Food]:
        """Populate with random food within bounds."""
        for i in range(amount):
            self.food.append(Food(
                x=random.randint(0, bounds[0]),
                y=random.randint(0, bounds[1]),
                size=10
            ))
        return self.food

    def eat(self, chr: Character) -> List[Food]:
        """Check if character hits any food, remove eaten food."""
        for f in self.food:
            if f.hit(chr):
                chr.eat()
                chr.resize()
                self.food.remove(f)
        return self.food

    def move(self, bounds: Tuple[int, int] = (1280, 720)) -> Self:
        """Randomly move all food items slightly."""
        for f in self.food:
            f.move(random.randint(-1, 1), random.randint(-1, 1))
            f.x = max(f.size, min(bounds[0] - f.size, f.x))
            f.y = max(f.size, min(bounds[1] - f.size, f.y))
        return self
