"""Test suite for game."""
import pygame
from cs110 import expect, summarize
import game
import player
import food
import opponent

# Setup
test_game = game.Game(
    screen     = pygame.display.set_mode((1280, 720)),
    clock      = pygame.time.Clock(),
    background = "purple",
    fps        = 60,
    running    = True,
    deltaT     = 0,
)


# Test game.tick
expect(test_game.tick(), test_game)


# Test player.move_to
test_player_move_mouse_1 = player.Player(x=150, y=200, size=10, speed=10, color="red")
test_player_move_mouse_2 = player.Player(x=0, y=0, size=10, speed=10, color="red")

test_player_mouse_1 = player.Player(x=150, y=100, size=10, speed=10, color="red")
test_player_mouse_2 = player.Player(x=100, y=100, size=10, speed=10, color="red")

expect(test_player_mouse_1.move_to((150, 200)), test_player_move_mouse_1)
expect(test_player_mouse_2.move_to((0, 0)), test_player_move_mouse_2)


# Test player.eat
test_player_eat = player.Player(x=100, y=100, size=10, speed=10, color="red", count=0)
test_player_eat.eat()
expect(test_player_eat.count, 1)
test_player_eat.eat()
expect(test_player_eat.count, 2)


# Test player.resize
test_player_resize = player.Player(x=100, y=100, size=10, speed=10, color="red", count=5)
test_player_resize.resize()
expect(test_player_resize.size, 15)
test_player_resize.eat()
test_player_resize.resize()
expect(test_player_resize.size, 16)


# Test Food.move
test_food_move_1 = food.Food(x=100, y=100, size=10)
test_food_move_2 = food.Food(x=100, y=100, size=10)
expect(test_food_move_1.move(5, -5), food.Food(x=105, y=95, size=10))
expect(test_food_move_2.move(-10, 10), food.Food(x=90, y=110, size=10))


# Test Food.distance
test_food_distance = food.Food(x=0, y=0, size=10)
test_player_dist = player.Player(x=0, y=10, size=10, speed=10, color="red")
expect(test_food_distance.distance(test_player_dist), 10.0)

test_player_dist_2 = player.Player(x=3, y=4, size=10, speed=10, color="red")
expect(test_food_distance.distance(test_player_dist_2), 5.0)


# Test Food.hit
test_food_hit = food.Food(x=0, y=0, size=1)
test_player_hit_1 = player.Player(x=0, y=10, size=10, speed=10, color="red")
test_player_hit_2 = player.Player(x=0, y=11, size=10, speed=10, color="red")
expect(test_food_hit.hit(test_player_hit_1), True)
expect(test_food_hit.hit(test_player_hit_2), False)


# Test FoodList.populate
test_food_list = food.FoodList([])
populated_food_list = test_food_list.populate(5, (500, 500))
expect(len(populated_food_list), 5)
for food_item in populated_food_list:
    expect(0 <= food_item.x <= 500, True)
    expect(0 <= food_item.y <= 500, True)


# Test FoodList.eat
test_food_list_eat = food.FoodList([food.Food(x=0, y=0, size=10)])
test_player_eat = player.Player(x=0, y=0, size=10, speed=10, color="red")
test_food_list_eat.eat(test_player_eat)
expect(len(test_food_list_eat.food), 0)
expect(test_player_eat.count, 1)


# Test FoodList.move
test_food_list_move = food.FoodList([food.Food(x=100, y=100, size=10), food.Food(x=100, y=100, size=10)])
test_food_list_move.move()
for food_item in test_food_list_move.food:
    expect(99 <= food_item.x <= 101, True)
    expect(99 <= food_item.y <= 101, True)


# Test Opponent.move
test_opponent_1 = opponent.Opponent(x=0, y=0, size=10, speed=100, color="green")
test_food_for_opponent = food.FoodList([food.Food(x=100, y=0, size=10)])
test_opponent_1.move(test_food_for_opponent, None, 1.0)
expect(test_opponent_1.x > 0, True)
expect(test_opponent_1.y, 0)


# Test Opponent.find_best_food
test_opponent_2 = opponent.Opponent(x=0, y=0, size=10, speed=10, color="green")
test_food_list_ai = food.FoodList([
    food.Food(x=50, y=0, size=10),
    food.Food(x=200, y=0, size=10)
])
best = test_opponent_2.find_best_food(test_food_list_ai)
expect(best.x, 50)


# Test with player position
test_opponent_3 = opponent.Opponent(x=100, y=0, size=10, speed=10, color="green")
test_food_contested = food.FoodList([
    food.Food(x=50, y=0, size=10),
    food.Food(x=90, y=0, size=10)
])
best_with_player = test_opponent_3.find_best_food(test_food_contested, player_pos=(45, 0))
expect(best_with_player.x, 90)


# Test Opponent.eat
test_opponent_eat = opponent.Opponent(x=100, y=100, size=10, speed=10, color="green", count=0)
test_opponent_eat.eat()
expect(test_opponent_eat.count, 1)
test_opponent_eat.resize()
expect(test_opponent_eat.size, 11)


# Test with empty food list
test_opponent_empty = opponent.Opponent(x=50, y=50, size=10, speed=10, color="green")
empty_food = food.FoodList([])
test_opponent_empty.move(empty_food)
expect(test_opponent_empty.x, 50)


# Lab 09: Food arithmetic
print("\n--- Lab 09: Food arithmetic ---")

f1 = food.Food(10, 20, 5)
f2 = food.Food(30, 40, 10)
f_add = f1 + f2
expect(f_add.x, 40)
expect(f_add.y, 60)
expect(f_add.size, 15)

f_sub = f2 - f1
expect(f_sub.x, 20)
expect(f_sub.size, 5)

f_mul = f1 * 2
expect(f_mul.x, 20)
expect(f_mul.size, 10)


# Food comparison
print("\n--- Lab 09: Food comparison ---")

expect(food.Food(10, 20, 5) == food.Food(10, 20, 5), True)
expect(food.Food(0, 0, 5) < food.Food(0, 0, 10), True)
expect(food.Food(0, 0, 10) > food.Food(0, 0, 5), True)

expect(food.Food(50, 50, 10).is_in_bounds((100, 100)), True)
expect(food.Food(150, 50, 10).is_in_bounds((100, 100)), False)
expect(food.Food(10, 10, 5).is_near((0, 0), 20), True)


# FoodList iteration
print("\n--- Lab 09: FoodList iteration ---")

fl = food.FoodList([food.Food(0, 0, 10), food.Food(1, 1, 5)])
expect(len(fl), 2)
expect(fl[0].size, 10)
sizes = [f.size for f in fl]
expect(sizes, [10, 5])
expect(food.FoodList([]).is_empty(), True)


# FoodList arithmetic
print("\n--- Lab 09: FoodList arithmetic ---")

fl1 = food.FoodList([food.Food(0, 0, 10)])
fl2 = food.FoodList([food.Food(1, 1, 5)])
combined = fl1 + fl2
expect(len(combined), 2)


# FoodList map
print("\n--- Lab 09: FoodList map ---")

fl_map = food.FoodList([food.Food(0, 0, 10), food.Food(10, 10, 5)])

mapped = fl_map.map(lambda f: food.Food(f.x, f.y, f.size * 2))
expect(mapped[0].size, 20)

grown = fl_map.grow_all(5)
expect(grown[0].size, 15)

shrunk = fl_map.shrink_all(3)
expect(shrunk[0].size, 7)

moved = fl_map.move_all(5, 10)
expect(moved[0].x, 5)


# FoodList filter
print("\n--- Lab 09: FoodList filter ---")

fl_filt = food.FoodList([
    food.Food(0, 0, 5),
    food.Food(50, 50, 10),
    food.Food(200, 200, 15)
])

filtered = fl_filt.filter(lambda f: f.size > 7)
expect(len(filtered), 2)

by_size = fl_filt.filter_by_size(6, 12)
expect(len(by_size), 1)

in_bounds = fl_filt.filter_in_bounds((100, 100))
expect(len(in_bounds), 2)


# FoodList reduce
print("\n--- Lab 09: FoodList reduce ---")

fl_red = food.FoodList([
    food.Food(0, 0, 10),
    food.Food(10, 10, 20),
    food.Food(20, 20, 30)
])

expect(fl_red.total_size(), 60.0)
expect(fl_red.average_size(), 20.0)

com = fl_red.center_of_mass()
expect(com[0], 10.0)

expect(fl_red.largest().size, 30)
expect(fl_red.smallest().size, 10)

closest = fl_red.closest_to((0, 0))
expect(closest.x, 0)

farthest = fl_red.farthest_from((0, 0))
expect(farthest.x, 20)

# empty list
fl_empty = food.FoodList([])
expect(fl_empty.total_size(), 0.0)
expect(fl_empty.largest(), None)


# FoodList logical
print("\n--- Lab 09: FoodList logical ---")

fl_log = food.FoodList([food.Food(50, 50, 10), food.Food(200, 200, 10)])
expect(fl_log.any_in_bounds((100, 100)), True)
expect(fl_log.all_in_bounds((100, 100)), False)
expect(fl_log.any_near((0, 0), 100), True)


# Done
summarize()
