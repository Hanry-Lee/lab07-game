"""Tests for food_parser."""

from cs110 import expect, summarize
from food_parser import *


# Test FoodTyped instantiation
food_typed = FoodTyped(
    food_id="food1",
    x=ScreenX(100.0),
    y=ScreenY(200.0),
    size=PositiveInt(10)
)

# Output some fields to demonstrate usage
print(f"Food ID: {food_typed.food_id}")
print(f"Position: ({food_typed.x.x}, {food_typed.y.y})")
print(f"Size: {food_typed.size.value}")
print()

# Test for parse_row_to_food
row = "food1,100,200,10"
expected_food = FoodTyped(
    food_id="food1",
    x=ScreenX(100.0),
    y=ScreenY(200.0),
    size=PositiveInt(10)
)
expect(parse_row_to_food(row), expected_food)

# Test for parse_row_to_food with different values
row2 = "food2,500,300,15"
expected_food2 = FoodTyped(
    food_id="food2",
    x=ScreenX(500.0),
    y=ScreenY(300.0),
    size=PositiveInt(15)
)
expect(parse_row_to_food(row2), expected_food2)

# Test for parse_foods with multiple rows
rows = [
    "food1,100,200,10",
    "food2,500,300,15",
    "food3,800,600,10"
]
expected_foods = [
    FoodTyped(food_id="food1", x=ScreenX(100.0), y=ScreenY(200.0), size=PositiveInt(10)),
    FoodTyped(food_id="food2", x=ScreenX(500.0), y=ScreenY(300.0), size=PositiveInt(15)),
    FoodTyped(food_id="food3", x=ScreenX(800.0), y=ScreenY(600.0), size=PositiveInt(10))
]
expect(parse_foods(rows), expected_foods)

# Test for query_foods
test_foods = parse_foods(rows)
expect(len(query_foods(test_foods, food_id="food1")), 1)
expect(len(query_foods(test_foods, food_id="invalid")), 0)

# Test for food_to_row
expect(food_to_row(expected_food), "food1,100.0,200.0,10")

# Test boundary values
food_corner = FoodTyped(
    food_id="corner",
    x=ScreenX(0),
    y=ScreenY(0),
    size=PositiveInt(5)
)
expect(food_corner.x.x, 0)
expect(food_corner.y.y, 0)

food_max = FoodTyped(
    food_id="max",
    x=ScreenX(1280),
    y=ScreenY(720),
    size=PositiveInt(5)
)
expect(food_max.x.x, 1280)
expect(food_max.y.y, 720)

summarize()
