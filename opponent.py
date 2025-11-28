"""A class for an Opponent."""
from dataclasses import dataclass
from typing import Tuple, Optional
from typing_extensions import Self
from character import Character
from food import Food, FoodList

@dataclass
class Opponent(Character):
    """A competing player with look-ahead AI."""
    current_target: Optional[Food] = None

    def find_best_food(self, food_list: FoodList, player_pos: Optional[Tuple[float, float]] = None) -> Optional[Food]:
        """Pick the best food to chase based on distance and clustering."""
        if not food_list.food:
            self.current_target = None
            return None

        if self.current_target and self.current_target in food_list.food:
            if self.current_target.distance(self) < 50:
                return self.current_target

        def score_food(f: Food) -> float:
            dist_to_self = f.distance(self)

            cluster_bonus = 0
            for other in food_list.food:
                if other != f:
                    d = ((f.x - other.x)**2 + (f.y - other.y)**2)**0.5
                    if d < 100:
                        cluster_bonus += (100 - d) * 0.1

            player_penalty = 0
            if player_pos:
                dist_to_player = ((f.x - player_pos[0])**2 + (f.y - player_pos[1])**2)**0.5
                if dist_to_player < dist_to_self:
                    player_penalty = (dist_to_self - dist_to_player) * 2

            return -dist_to_self + cluster_bonus - player_penalty

        self.current_target = max(food_list.food, key=score_food)
        return self.current_target

    def move(self, food_list: FoodList, player_pos: Optional[Tuple[float, float]] = None, deltaT: float = 1/60) -> Self:
        target = self.find_best_food(food_list, player_pos)
        if not target:
            return self
        direction = self.direction(target)
        self.x = self.x + (self.speed * direction[0] * deltaT)
        self.y = self.y + (self.speed * direction[1] * deltaT)
        return self
            
