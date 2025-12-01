# Lab 09: Map-Reduce and Recursion

## Individual Part

### shape_parser.py
Parses GTFS shapes.txt into LinkedList data structures.

**Data Structures:**
- `Node`: linked list node with data and next pointer
- `LinkedList`: wrapper class holding head node
- `ShapeLinkedList`: specialized LinkedList that keeps shapes sorted by sequence

**Parsing (uses map, filter, reduce - single file traversal):**
- `parse_row_to_shape`: map function converting CSV rows to Shape objects
- `add_shape_to_lists`: reduce function grouping shapes by id
- `parse_shapes_file`: main parser using map -> filter -> reduce pipeline

**Recursive Distance Calculation:**
- `node_distance`: recursive function to sum distances along linked list
  - Base case: n.next is None -> return 0
  - Recursive step: distance to next + node_distance(n.next)
- `haversine_distance`: calculates distance between lat/lon points

**Route Analysis (uses map, filter, reduce):**
- `get_longest_route`: finds shape with maximum total distance
- `get_shortest_route`: finds shape with minimum total distance
- `get_average_route_length`: calculates mean distance across all shapes
- `get_routes_longer_than`: filters shapes exceeding threshold

### shape_parser_tests.py
Test suite covering all functions with examples.

---

## Group Part

Building on Week 8 game design, added map/filter/reduce helpers and arithmetic/logical operations.

### food.py - Food and FoodList classes

**Food Arithmetic:**
- `__add__`: combine two foods (positions and sizes)
- `__sub__`: difference between foods
- `__mul__`: scale food by factor

**Food Comparison:**
- `__eq__`, `__lt__`, `__le__`, `__gt__`, `__ge__`: compare by size
- `is_in_bounds`: check if within screen bounds
- `is_near`: check if within radius of point

**FoodList Map Operations:**
- `map`: apply function to each food
- `grow_all`, `shrink_all`, `scale_all`: size transformations
- `move_all`: translate all food by offset

**FoodList Filter Operations:**
- `filter`: keep foods matching predicate
- `filter_by_size`: keep foods in size range
- `filter_in_bounds`: keep foods within bounds
- `filter_near`: keep foods near point
- `filter_hittable_by`: keep foods that sprite can hit

**FoodList Reduce Operations:**
- `reduce`: generic reduce function
- `total_size`, `average_size`: aggregate calculations
- `center_of_mass`: average position
- `largest`, `smallest`: find extremes
- `closest_to`, `farthest_from`: find by distance

**FoodList Logical Operations:**
- `any_in_bounds`, `all_in_bounds`: bounds checks
- `any_near`: proximity check
- `is_empty`: empty check

### tests.py
Test suite covering all new functionality (74 tests total).

---

## Files

- shape_parser.py - LinkedList parser (individual)
- shape_parser_tests.py - parser tests
- shapes.txt - sample GTFS data
- food.py - Food/FoodList with map/filter/reduce (group)
- sprite.py, character.py, player.py, opponent.py, game.py - game classes
- tests.py - game tests
- cs110.py - test framework
