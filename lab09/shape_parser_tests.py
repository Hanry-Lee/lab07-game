"""Tests for shape_parser.py"""
from cs110 import expect
from shape_parser import (
    Shape, Node, LinkedList, ShapeLinkedList,
    parse_row_to_shape, add_shape_to_lists, parse_shapes_file,
    haversine_distance, node_distance, calculate_shape_distance,
    get_longest_route, get_shortest_route, get_average_route_length,
    get_routes_longer_than
)


# Shape tests
print("Testing Shape...")

shape1 = Shape("1", 49.286458, -123.140424, 1, 0.0)
expect(shape1.id, "1")
expect(shape1.lat, 49.286458)
expect(shape1.lon, -123.140424)
expect(shape1.sequence, 1)


# Node tests
print("Testing Node...")

n0 = Node(0, None)
expect(n0.data, 0)
expect(n0.next, None)

n1 = Node(1, n0)
expect(n1.next, n0)

n2 = Node(2, n1)
n3 = Node(3, n2)
expect(n3.next.next, n1)


# LinkedList tests
print("Testing LinkedList...")

ll = LinkedList()
expect(ll.head, None)


# ShapeLinkedList tests
print("Testing ShapeLinkedList...")

sll_empty = ShapeLinkedList(shape_id="1")
expect(sll_empty.head, None)
expect(len(sll_empty), 0)

sll1 = ShapeLinkedList(shape_id="1")
sll1.add(Shape("1", 49.0, -123.0, 1, 0.0))
expect(len(sll1), 1)

# test sorted insertion
sll2 = ShapeLinkedList(shape_id="2")
sll2.add(Shape("2", 49.0, -123.0, 1, 0.0))
sll2.add(Shape("2", 49.1, -123.1, 2, 100.0))
sll2.add(Shape("2", 49.2, -123.2, 3, 200.0))
expect(len(sll2), 3)
expect(sll2.head.data.sequence, 1)

# out of order insertion
sll3 = ShapeLinkedList(shape_id="3")
sll3.add(Shape("3", 49.2, -123.2, 3, 200.0))
sll3.add(Shape("3", 49.0, -123.0, 1, 0.0))
sll3.add(Shape("3", 49.1, -123.1, 2, 100.0))
expect(sll3.head.data.sequence, 1)
expect(sll3.head.next.data.sequence, 2)
expect(sll3.head.next.next.data.sequence, 3)

# test to_list and iteration
expect(len(sll3.to_list()), 3)
seqs = [s.sequence for s in sll3]
expect(seqs, [1, 2, 3])


# parse_row tests
print("Testing parse_row_to_shape...")

row = {
    "shape_id": "1",
    "shape_pt_lat": "49.286458",
    "shape_pt_lon": "-123.140424",
    "shape_pt_sequence": "1",
    "shape_dist_traveled": "0.0"
}
parsed = parse_row_to_shape(row)
expect(parsed.id, "1")
expect(parsed.sequence, 1)


# add_shape_to_lists tests
print("Testing add_shape_to_lists...")

d = {}
s1 = Shape("1", 49.0, -123.0, 1, 0.0)
result = add_shape_to_lists(d, s1)
expect("1" in result, True)
expect(len(result["1"]), 1)


# haversine tests
print("Testing haversine_distance...")

d0 = haversine_distance(49.0, -123.0, 49.0, -123.0)
expect(d0, 0.0)

d1 = haversine_distance(49.0, -123.0, 49.001, -123.0)
expect(100 < d1 < 150, True)


# recursive distance tests
print("Testing node_distance (recursive)...")

single = Node(Shape("1", 49.0, -123.0, 1, 0.0), None)
expect(node_distance(single), 0.0)

na = Node(Shape("1", 49.0, -123.0, 1, 0.0), None)
nb = Node(Shape("1", 49.001, -123.0, 2, 100.0), na)
d_two = node_distance(nb)
expect(d_two > 0, True)

nc = Node(Shape("1", 49.002, -123.0, 3, 200.0), nb)
d_three = node_distance(nc)
expect(d_three > d_two, True)


# calculate_shape_distance tests
print("Testing calculate_shape_distance...")

empty_sll = ShapeLinkedList(shape_id="empty")
expect(calculate_shape_distance(empty_sll), 0.0)

single_sll = ShapeLinkedList(shape_id="single")
single_sll.add(Shape("single", 49.0, -123.0, 1, 0.0))
expect(calculate_shape_distance(single_sll), 0.0)


# route analysis tests
print("Testing route analysis...")

short_route = ShapeLinkedList(shape_id="short")
short_route.add(Shape("short", 49.0, -123.0, 1, 0.0))
short_route.add(Shape("short", 49.001, -123.0, 2, 100.0))

medium_route = ShapeLinkedList(shape_id="medium")
medium_route.add(Shape("medium", 49.0, -123.0, 1, 0.0))
medium_route.add(Shape("medium", 49.002, -123.0, 2, 200.0))
medium_route.add(Shape("medium", 49.004, -123.0, 3, 400.0))

long_route = ShapeLinkedList(shape_id="long")
long_route.add(Shape("long", 49.0, -123.0, 1, 0.0))
long_route.add(Shape("long", 49.003, -123.0, 2, 300.0))
long_route.add(Shape("long", 49.006, -123.0, 3, 600.0))
long_route.add(Shape("long", 49.009, -123.0, 4, 900.0))

test_lists = [short_route, medium_route, long_route]

# longest
expect(get_longest_route([]), None)
longest = get_longest_route(test_lists)
expect(longest.shape_id, "long")

# shortest
expect(get_shortest_route([]), None)
shortest = get_shortest_route(test_lists)
expect(shortest.shape_id, "short")

# average
expect(get_average_route_length([]), 0.0)
avg = get_average_route_length(test_lists)
expect(avg > 0, True)

short_d = calculate_shape_distance(short_route)
long_d = calculate_shape_distance(long_route)
expect(short_d < avg < long_d, True)

# filter by distance
expect(get_routes_longer_than([], 100.0), [])
medium_d = calculate_shape_distance(medium_route)
longer = get_routes_longer_than(test_lists, medium_d)
expect(len(longer), 1)
expect(longer[0].shape_id, "long")


# integration test
print("Testing file parsing...")

try:
    lists = parse_shapes_file("shapes.txt")
    expect(len(lists) >= 1, True)

    for sl in lists:
        expect(sl.shape_id != "", True)
        prev = 0
        for s in sl:
            expect(s.sequence > prev, True)
            prev = s.sequence

    print(f"Parsed {len(lists)} shapes from file")
except FileNotFoundError:
    print("shapes.txt not found, skipping")


print("\nAll tests done!")
