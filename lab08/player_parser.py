"""Parses player.csv for game state."""
from typing import List
from dataclasses import dataclass

# Reuse Range class pattern from stop_parser.py
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


@dataclass
class Range:
    """Class to validate if a given value is within a specified range."""
    def validate(self, value:     float | int,
                       min_value: float | int,
                       max_value: float | int) -> float | int | None:
        """
        Purpose: Validates if the value is within the specified min and max range.
        Example:
            validate(10,0,10) -> True
            validate(10,0, 9) -> False
        """
        if not (min_value <= value <= max_value):
            raise ValueError(
                f"Value {value} is out of range [{min_value}, {max_value}]"
            )
        return value


@dataclass
class ScreenX(Range):
    """Class to validate x position on screen."""
    def __init__(self, x: float) -> None:
        self.x = self.validate(x, 0, SCREEN_WIDTH)  # x must be in range [0, SCREEN_WIDTH]


@dataclass
class ScreenY(Range):
    """Class to validate y position on screen."""
    def __init__(self, y: float) -> None:
        self.y = self.validate(y, 0, SCREEN_HEIGHT)  # y must be in range [0, SCREEN_HEIGHT]


@dataclass
class PositiveInt(Range):
    """Class to validate non-negative integer."""
    def __init__(self, value: int) -> None:
        self.value = self.validate(value, 0, float('inf'))


@dataclass
class PositiveFloat(Range):
    """Class to validate non-negative float."""
    def __init__(self, value: float) -> None:
        self.value = self.validate(value, 0, float('inf'))


@dataclass
class Color:
    """Class to validate color names."""
    VALID_COLORS = {'red', 'blue', 'green', 'yellow', 'white', 'black',
                    'orange', 'purple', 'pink', 'cyan', 'magenta', 'gray'}

    def __init__(self, color: str) -> None:
        if self.validate(color):
            self.color = color.lower()
        else:
            raise ValueError(f"Invalid color: {color}")

    def validate(self, color: str) -> bool:
        """
        Purpose: Validates if the given string is a valid color name.
        Example:
            validate("red") -> True
            validate("invalid") -> False
        """
        return color.lower() in self.VALID_COLORS


@dataclass
class Player:
    """Raw data model for player from player.csv."""
    player_id: str       # Unique ID
    x: float             # X position
    y: float             # Y position
    size: int            # Size of player
    speed: float         # Movement speed
    color: str           # Color
    count: int           # Food eaten


@dataclass
class PlayerTyped:
    """Typed data model with validated fields."""
    player_id: str
    x: ScreenX
    y: ScreenY
    size: PositiveInt
    speed: PositiveFloat
    color: Color
    count: PositiveInt

    def __str__(self) -> str:
        """
        Purpose: Pretty-print the PlayerTyped instance.

        Example:
            Player ID: player1
            Position: (100, 200)
            Size: 10
        """
        return (f"Player ID: {self.player_id}\n"
                f"Position: ({self.x.x}, {self.y.y})\n"
                f"Size: {self.size.value}\n"
                f"Speed: {self.speed.value}\n"
                f"Color: {self.color.color}\n"
                f"Count: {self.count.value}\n")


def parse_screen_x(value: str) -> ScreenX:
    """
    Purpose: Convert a string to ScreenX.
    Example: parse_screen_x("100") -> ScreenX(100.0)
    """
    return ScreenX(float(value))


def parse_screen_y(value: str) -> ScreenY:
    """
    Purpose: Convert a string to ScreenY.
    Example: parse_screen_y("200") -> ScreenY(200.0)
    """
    return ScreenY(float(value))


def parse_positive_int(value: str) -> PositiveInt:
    """
    Purpose: Convert string to PositiveInt.
    Example: parse_positive_int("10") -> PositiveInt(10)
    """
    return PositiveInt(int(value))


def parse_positive_float(value: str) -> PositiveFloat:
    """
    Purpose: Convert string to PositiveFloat.
    Example: parse_positive_float("5.0") -> PositiveFloat(5.0)
    """
    return PositiveFloat(float(value))


def parse_color(value: str) -> Color:
    """
    Purpose: Convert string to Color.
    Example: parse_color("red") -> Color("red")
    """
    return Color(value)

def parse_row_to_player(row: str) -> PlayerTyped:
    """
    Purpose: Convert a comma-separated string row into a PlayerTyped instance.
    Example:
        parse_row_to_player("player1,100,200,10,5.0,red,3")
            -> PlayerTyped(player_id="player1", ...)
    """
    columns = row.strip().split(',')

    player_id = columns[0]
    x = parse_screen_x(columns[1])
    y = parse_screen_y(columns[2])
    size = parse_positive_int(columns[3])
    speed = parse_positive_float(columns[4])
    color = parse_color(columns[5])
    count = parse_positive_int(columns[6])

    return PlayerTyped(
        player_id=player_id,
        x=x,
        y=y,
        size=size,
        speed=speed,
        color=color,
        count=count
    )

def parse_players(rows: List[str]) -> List[PlayerTyped]:
    """
    Purpose: Parse multiple rows into a list of PlayerTyped instances.
    Example:
        parse_players(["player1,100,200,10,5.0,red,3"]) -> [PlayerTyped(...)]
    """
    return [parse_row_to_player(row) for row in rows]


def query_players(players: list[PlayerTyped], **filters) -> list[PlayerTyped]:
    """
    Purpose: Query the list of players based on filters.
    Example:
        query_players(players, player_id="player1") -> list of matching PlayerTyped
    """
    results = players
    for attr, value in filters.items():
        results = [p for p in results if getattr(p, attr) == value]
    return results


def player_to_row(player: PlayerTyped) -> str:
    """
    Purpose: Convert a PlayerTyped instance to a CSV row string.
    Example:
        player_to_row(PlayerTyped(...)) -> "player1,100,200,10,5.0,red,3"
    """
    return f"{player.player_id},{player.x.x},{player.y.y},{player.size.value},{player.speed.value},{player.color.color},{player.count.value}"


def write_players_csv(filepath: str, players: List[PlayerTyped]) -> None:
    """
    Purpose: Write a list of PlayerTyped instances to a CSV file.
    Example:
        write_players_csv("player.csv", [player1, player2])
    """
    header = "player_id,x,y,size,speed,color,count"
    with open(filepath, 'w') as f:
        f.write(header + '\n')
        for player in players:
            f.write(player_to_row(player) + '\n')


def read_players_csv(filepath: str) -> List[PlayerTyped]:
    """
    Purpose: Read a CSV file and return a list of PlayerTyped instances.
    Example:
        read_players_csv("player.csv") -> [PlayerTyped(...), ...]
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()
        return parse_players(lines[1:])  # Skip header


if __name__ == "__main__":
    example_row = "player1,100,200,10,5.0,red,3"
    player = parse_row_to_player(example_row)
    print(player)
