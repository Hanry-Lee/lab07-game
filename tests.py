"""Test suite for game."""
import pygame
from cs110 import expect, summarize
import game
import player
import food
import opponent

#------------------------------------------------------------------------------#
# Setup: Run these before all tests.
#------------------------------------------------------------------------------#
test_game = game.Game(
        screen     = pygame.display.set_mode((1280, 720)),
        clock      = pygame.time.Clock(),
        background = "purple",
        fps        = 60,
        running    = True,
        deltaT     = 0,
    )


#------------------------------------------------------------------------------#
# Test game.tick
#------------------------------------------------------------------------------#
expect(test_game.tick(), test_game)


#------------------------------------------------------------------------------#
# Test player.move_to
#------------------------------------------------------------------------------#
test_player_move_mouse_1 = player.Player(x=150, y=200, size=10, speed=10, color="red")
test_player_move_mouse_2 = player.Player(x=0, y=0, size=10, speed=10, color="red")

test_player_mouse_1 = player.Player(x=150, y=100, size=10, speed=10, color="red")
test_player_mouse_2 = player.Player(x=100, y=100, size=10, speed=10, color="red")

# Move player to (150, 200) and (0, 0)
expect(test_player_mouse_1.move_to((150, 200)), test_player_move_mouse_1)
expect(test_player_mouse_2.move_to((0, 0)), test_player_move_mouse_2)


#------------------------------------------------------------------------------#
# Test player.eat
#------------------------------------------------------------------------------#
test_player_eat = player.Player(x=100, y=100, size=10, speed=10, color="red", count=0)

# Eat food and increment count
test_player_eat.eat()
expect(test_player_eat.count, 1)

# Eat again and increment count
test_player_eat.eat()
expect(test_player_eat.count, 2)


#------------------------------------------------------------------------------#
# Test player.resize
#------------------------------------------------------------------------------#
test_player_resize = player.Player(x=100, y=100, size=10, speed=10, color="red", count=5)
test_player_resize.resize()

# After resizing, size should be 10 + count (i.e., 15)
expect(test_player_resize.size, 15)

# Simulate eating food and resizing
test_player_resize.eat()
test_player_resize.resize()
expect(test_player_resize.size, 16)


#------------------------------------------------------------------------------#
# Test Food.move
#------------------------------------------------------------------------------#
test_food_move_1 = food.Food(x=100, y=100, size=10)
test_food_move_2 = food.Food(x=100, y=100, size=10)

# Move the food by (5, -5) and (-10, 10)
expect(test_food_move_1.move(5, -5), food.Food(x=105, y=95, size=10))
expect(test_food_move_2.move(-10, 10), food.Food(x=90, y=110, size=10))


#------------------------------------------------------------------------------#
# Test Food.distance
#------------------------------------------------------------------------------#
test_food_distance = food.Food(x=0, y=0, size=10)
test_player_dist = player.Player(x=0, y=10, size=10, speed=10, color="red")

# Calculate the distance between food and player
expect(test_food_distance.distance(test_player_dist), 10.0)

test_player_dist_2 = player.Player(x=3, y=4, size=10, speed=10, color="red")
# Calculate the distance between food and player (Pythagoras: 3^2 + 4^2 = 5^2)
expect(test_food_distance.distance(test_player_dist_2), 5.0)


#------------------------------------------------------------------------------#
# Test Food.hit
#------------------------------------------------------------------------------#
test_food_hit = food.Food(x=0, y=0, size=1)
test_player_hit_1 = player.Player(x=0, y=10, size=10, speed=10, color="red")
test_player_hit_2 = player.Player(x=0, y=11, size=10, speed=10, color="red")

# Player 1 should hit the food
expect(test_food_hit.hit(test_player_hit_1), True)

# Player 2 should not hit the food
expect(test_food_hit.hit(test_player_hit_2), False)

#------------------------------------------------------------------------------#
# Test FoodList.populate
#------------------------------------------------------------------------------#
test_food_list = food.FoodList([])

# Populate with 5 food items within bounds (500, 500)
populated_food_list = test_food_list.populate(5, (500, 500))

# Expect 5 items in the list
expect(len(populated_food_list), 5)

# Check that all food items are within bounds
for food_item in populated_food_list:
    expect(0 <= food_item.x <= 500, True)
    expect(0 <= food_item.y <= 500, True)
    expect(food_item.size, 10)


#------------------------------------------------------------------------------#
# Test FoodList.eat
#------------------------------------------------------------------------------#
test_food_list_eat = food.FoodList([food.Food(x=0, y=0, size=10)])
test_player_eat = player.Player(x=0, y=0, size=10, speed=10, color="red")

# Player eats the food, expect the list to be empty and player count to increase
test_food_list_eat.eat(test_player_eat)
expect(len(test_food_list_eat.food), 0)
expect(test_player_eat.count, 1)
expect(test_player_eat.size, 11)  # Size should increase after eating


#------------------------------------------------------------------------------#
# Test FoodList.move
#------------------------------------------------------------------------------#
test_food_list_move = food.FoodList([food.Food(x=100, y=100, size=10), food.Food(x=100, y=100, size=10)])

# Move the food items in the list
test_food_list_move.move()

# Expect the food items to have moved slightly
for food_item in test_food_list_move.food:
    expect(99 <= food_item.x <= 101, True)
    expect(99 <= food_item.y <= 101, True)


#------------------------------------------------------------------------------#
# Test Opponent.move
#------------------------------------------------------------------------------#
test_opponent_1 = opponent.Opponent(x=0, y=0, size=10, speed=100, color="green")
test_food_for_opponent = food.FoodList([food.Food(x=100, y=0, size=10)])

test_opponent_1.move(test_food_for_opponent, None, 1.0)
expect(test_opponent_1.x > 0, True)
expect(test_opponent_1.y, 0)

#------------------------------------------------------------------------------#
# Test Opponent.find_best_food
#------------------------------------------------------------------------------#
test_opponent_2 = opponent.Opponent(x=0, y=0, size=10, speed=10, color="green")
test_food_list_ai = food.FoodList([
    food.Food(x=50, y=0, size=10),
    food.Food(x=200, y=0, size=10)
])

best = test_opponent_2.find_best_food(test_food_list_ai)
expect(best.x, 50)

#------------------------------------------------------------------------------#
# Test Opponent.find_best_food with player position
#------------------------------------------------------------------------------#
test_opponent_3 = opponent.Opponent(x=100, y=0, size=10, speed=10, color="green")
test_food_contested = food.FoodList([
    food.Food(x=50, y=0, size=10),
    food.Food(x=90, y=0, size=10)
])

best_with_player = test_opponent_3.find_best_food(test_food_contested, player_pos=(45, 0))
expect(best_with_player.x, 90)

#------------------------------------------------------------------------------#
# Test Opponent.eat and resize
#------------------------------------------------------------------------------#
test_opponent_eat = opponent.Opponent(x=100, y=100, size=10, speed=10, color="green", count=0)
test_opponent_eat.eat()
expect(test_opponent_eat.count, 1)
test_opponent_eat.resize()
expect(test_opponent_eat.size, 11)

#------------------------------------------------------------------------------#
# Test Opponent with empty food list
#------------------------------------------------------------------------------#
test_opponent_empty = opponent.Opponent(x=50, y=50, size=10, speed=10, color="green")
empty_food = food.FoodList([])
test_opponent_empty.move(empty_food)
expect(test_opponent_empty.x, 50)
expect(test_opponent_empty.y, 50)

#------------------------------------------------------------------------------#
# Summarize the tests
#------------------------------------------------------------------------------#
summarize()