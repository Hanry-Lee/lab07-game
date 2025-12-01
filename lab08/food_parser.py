"""Parses food.csv for game state."""
from typing import List
from dataclasses import dataclass

# Import reusable validation classes from player_parser
from player_parser import ScreenX, ScreenY, PositiveInt, parse_screen_x, parse_screen_y, parse_positive_int


@dataclass
class Food:
    """Raw data model for food from food.csv."""
    food_id: str    # Unique ID
    x: float        # X position
    y: float        # Y position
    size: int       # Size


@dataclass
class FoodTyped:
    """Typed data model with validated fields."""
    food_id: str
    x: ScreenX
    y: ScreenY
    size: PositiveInt

    def __str__(self) -> str:
        """
        Purpose: Pretty-print the FoodTyped instance.

        Example:
            Food ID: food1
            Position: (100, 200)
            Size: 10
        """
        return (f"Food ID: {self.food_id}\n"
                f"Position: ({self.x.x}, {self.y.y})\n"
                f"Size: {self.size.value}\n")


def parse_row_to_food(row: str) -> FoodTyped:
    """
    Purpose: Convert a comma-separated string row into a FoodTyped instance.
    Example:
        parse_row_to_food("food1,100,200,10")
            -> FoodTyped(food_id="food1", x=ScreenX(100), ...)
    """
    columns = row.strip().split(',')

    food_id = columns[0]
    x = parse_screen_x(columns[1])
    y = parse_screen_y(columns[2])
    size = parse_positive_int(columns[3])

    return FoodTyped(
        food_id=food_id,
        x=x,
        y=y,
        size=size
    )

def parse_foods(rows: List[str]) -> List[FoodTyped]:
    """
    Purpose: Parse multiple rows into a list of FoodTyped instances.
    Example:
        parse_foods(["food1,100,200,10"]) -> [FoodTyped(...)]
    """
    return [parse_row_to_food(row) for row in rows]


def query_foods(foods: list[FoodTyped], **filters) -> list[FoodTyped]:
    """
    Purpose: Query the list of foods based on filters.
    Example:
        query_foods(foods, food_id="food1") -> list of matching FoodTyped
    """
    results = foods
    for attr, value in filters.items():
        results = [f for f in results if getattr(f, attr) == value]
    return results


def food_to_row(food: FoodTyped) -> str:
    """
    Purpose: Convert a FoodTyped instance to a CSV row string.
    Example:
        food_to_row(FoodTyped(...)) -> "food1,100,200,10"
    """
    return f"{food.food_id},{food.x.x},{food.y.y},{food.size.value}"


def write_foods_csv(filepath: str, foods: List[FoodTyped]) -> None:
    """
    Purpose: Write a list of FoodTyped instances to a CSV file.
    Example:
        write_foods_csv("food.csv", [food1, food2])
    """
    header = "food_id,x,y,size"
    with open(filepath, 'w') as f:
        f.write(header + '\n')
        for food in foods:
            f.write(food_to_row(food) + '\n')


def read_foods_csv(filepath: str) -> List[FoodTyped]:
    """
    Purpose: Read a CSV file and return a list of FoodTyped instances.
    Example:
        read_foods_csv("food.csv") -> [FoodTyped(...), ...]
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()
        return parse_foods(lines[1:])  # Skip header


if __name__ == "__main__":
    example_row = "food1,100,200,10"
    food = parse_row_to_food(example_row)
    print(food)
