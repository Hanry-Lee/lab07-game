"""Save and load game state to file."""
import json
from typing import Dict, Any

def save_game(filepath: str, player, opponent, food_list) -> None:
    state = {
        "player": {"x": player.x, "y": player.y, "size": player.size, "speed": player.speed, "color": player.color, "count": player.count},
        "opponent": {"x": opponent.x, "y": opponent.y, "size": opponent.size, "speed": opponent.speed, "color": opponent.color, "count": opponent.count},
        "food": [{"x": f.x, "y": f.y, "size": f.size} for f in food_list.food]
    }
    with open(filepath, 'w') as f:
        json.dump(state, f)

def load_game(filepath: str) -> Dict[str, Any]:
    with open(filepath, 'r') as f:
        return json.load(f)
