"""Game state manager using CSV format."""
from typing import List, Dict, Any
from dataclasses import dataclass

from player_parser import (
    PlayerTyped, ScreenX, ScreenY, PositiveInt, PositiveFloat, Color,
    write_players_csv, read_players_csv
)
from food_parser import (
    FoodTyped, write_foods_csv, read_foods_csv
)


@dataclass
class GameState:
    """Container for complete game state."""
    player: PlayerTyped
    opponent: PlayerTyped
    foods: List[FoodTyped]

    def __str__(self) -> str:
        return (f"=== Game State ===\n"
                f"--- Player ---\n{self.player}"
                f"--- Opponent ---\n{self.opponent}"
                f"--- Foods ({len(self.foods)} items) ---\n")


def save_game_state(directory: str, state: GameState) -> None:
    """
    Purpose: Save game state to CSV files.
    Example:
        save_game_state("saves/", game_state)
    """
    players = [state.player, state.opponent]
    write_players_csv(f"{directory}/player.csv", players)
    write_foods_csv(f"{directory}/food.csv", state.foods)


def load_game_state(directory: str) -> GameState:
    """
    Purpose: Load game state from CSV files.
    Example:
        state = load_game_state("saves/")
    """
    players = read_players_csv(f"{directory}/player.csv")
    player = players[0] if len(players) > 0 else None
    opponent = players[1] if len(players) > 1 else None
    foods = read_foods_csv(f"{directory}/food.csv")
    return GameState(player=player, opponent=opponent, foods=foods)


def player_to_typed(player_id: str, player) -> PlayerTyped:
    """
    Purpose: Convert a game Player object to PlayerTyped.
    Example:
        typed = player_to_typed("player1", game_player)
    """
    return PlayerTyped(
        player_id=player_id,
        x=ScreenX(float(player.x)),
        y=ScreenY(float(player.y)),
        size=PositiveInt(int(player.size)),
        speed=PositiveFloat(float(player.speed)),
        color=Color(player.color),
        count=PositiveInt(int(player.count))
    )


def food_to_typed(food_id: str, food) -> FoodTyped:
    """
    Purpose: Convert a game Food object to FoodTyped.
    Example:
        typed = food_to_typed("food1", game_food)
    """
    return FoodTyped(
        food_id=food_id,
        x=ScreenX(float(food.x)),
        y=ScreenY(float(food.y)),
        size=PositiveInt(int(food.size))
    )


def typed_to_dict(player: PlayerTyped) -> Dict[str, Any]:
    """Convert PlayerTyped to dict for game reconstruction."""
    return {
        "x": player.x.x,
        "y": player.y.y,
        "size": player.size.value,
        "speed": player.speed.value,
        "color": player.color.color,
        "count": player.count.value
    }


def food_typed_to_dict(food: FoodTyped) -> Dict[str, Any]:
    """Convert FoodTyped to dict for game reconstruction."""
    return {
        "x": food.x.x,
        "y": food.y.y,
        "size": food.size.value
    }


if __name__ == "__main__":
    print("Game State CSV Manager")
    print("Use save_game_state() and load_game_state() to manage saves.")
