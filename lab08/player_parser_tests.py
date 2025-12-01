"""Tests for player_parser."""

from cs110 import expect, summarize
from player_parser import *


# Test ScreenX validation
screen_x_valid = ScreenX(100.0)
screen_x_zero = ScreenX(0)
screen_x_max = ScreenX(1280)

# Test ScreenY validation
screen_y_valid = ScreenY(200.0)
screen_y_zero = ScreenY(0)
screen_y_max = ScreenY(720)

# Test PositiveInt validation
pos_int = PositiveInt(10)
pos_int_zero = PositiveInt(0)

# Test PositiveFloat validation
pos_float = PositiveFloat(5.5)
pos_float_zero = PositiveFloat(0.0)

# Test Color validation
color_red = Color("red")
color_blue = Color("BLUE")  # Should be case-insensitive

# Example instantiation of PlayerTyped
player_typed = PlayerTyped(
    player_id="player1",
    x=ScreenX(100.0),
    y=ScreenY(200.0),
    size=PositiveInt(10),
    speed=PositiveFloat(5.0),
    color=Color("red"),
    count=PositiveInt(3)
)

# Output some fields to demonstrate usage
print(f"Player ID: {player_typed.player_id}")
print(f"Position: ({player_typed.x.x}, {player_typed.y.y})")
print(f"Color: {player_typed.color.color}")
print()

# Test for parse_screen_x
expect(parse_screen_x("100").x, 100.0)
expect(parse_screen_x("0").x, 0.0)
expect(parse_screen_x("1280").x, 1280.0)

# Test for parse_screen_y
expect(parse_screen_y("200").y, 200.0)
expect(parse_screen_y("0").y, 0.0)
expect(parse_screen_y("720").y, 720.0)

# Test for parse_positive_int
expect(parse_positive_int("10").value, 10)
expect(parse_positive_int("0").value, 0)

# Test for parse_positive_float
expect(parse_positive_float("5.5").value, 5.5)
expect(parse_positive_float("0.0").value, 0.0)

# Test for parse_color
expect(parse_color("red").color, "red")
expect(parse_color("BLUE").color, "blue")
expect(parse_color("Green").color, "green")

# Test for Color validation
expect(Color("red").validate("red"), True)
expect(Color("blue").validate("invalid"), False)

# Test for parse_row_to_player
row = "player1,100,200,10,5.0,red,3"
expected_player = PlayerTyped(
    player_id="player1",
    x=ScreenX(100.0),
    y=ScreenY(200.0),
    size=PositiveInt(10),
    speed=PositiveFloat(5.0),
    color=Color("red"),
    count=PositiveInt(3)
)
expect(parse_row_to_player(row), expected_player)

# Test for parse_row_to_player with opponent
row_opponent = "opponent1,300,400,15,3.0,blue,5"
expected_opponent = PlayerTyped(
    player_id="opponent1",
    x=ScreenX(300.0),
    y=ScreenY(400.0),
    size=PositiveInt(15),
    speed=PositiveFloat(3.0),
    color=Color("blue"),
    count=PositiveInt(5)
)
expect(parse_row_to_player(row_opponent), expected_opponent)

# Test for parse_players with multiple rows
rows = [
    "player1,100,200,10,5.0,red,3",
    "opponent1,300,400,15,3.0,blue,5"
]
expected_players = [expected_player, expected_opponent]
expect(parse_players(rows), expected_players)

# Test for query_players
test_players = parse_players(rows)
expect(len(query_players(test_players, player_id="player1")), 1)
expect(len(query_players(test_players, player_id="invalid")), 0)

# Test for player_to_row
expect(player_to_row(expected_player), "player1,100.0,200.0,10,5.0,red,3")

summarize()
