"""
Lab 09: Shape Parser
Parses GTFS shapes.txt into LinkedLists grouped by shape_id
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Self, Optional
from functools import reduce
import csv
import math


@dataclass
class Shape:
    """A shape point from GTFS shapes.txt"""
    id: str
    lat: float
    lon: float
    sequence: int
    dist_traveled: float


@dataclass
class Node:
    """
    A node in a linked list.

    @dataclass
    class Node:
        data: Any
        next: Self
    """
    data: Any
    next: Optional[Self] = None


@dataclass
class LinkedList:
    """Wrapper class for linked list - holds the head node."""
    head: Optional[Node] = None


@dataclass
class ShapeLinkedList(LinkedList):
    """
    LinkedList for shapes with the same id.
    Keeps shapes sorted by sequence number.
    """
    shape_id: str = ""
    _length: int = field(default=0, repr=False)

    def add(self, shape: Shape) -> None:
        """
        Add a shape in the correct sequence position.

        Example:
            sll = ShapeLinkedList("1")
            sll.add(Shape("1", 49.0, -123.0, 2, 100.0))
            sll.add(Shape("1", 49.1, -123.1, 1, 0.0))
            # head should be sequence 1, then sequence 2
        """
        new_node = Node(shape)
        self._length += 1

        if self.head is None:
            self.head = new_node
            return

        # insert at beginning
        if shape.sequence < self.head.data.sequence:
            new_node.next = self.head
            self.head = new_node
            return

        # find spot to insert
        current = self.head
        while current.next is not None:
            if shape.sequence < current.next.data.sequence:
                new_node.next = current.next
                current.next = new_node
                return
            current = current.next

        current.next = new_node

    def __len__(self) -> int:
        return self._length

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.data
            current = current.next

    def to_list(self) -> list[Shape]:
        return list(self)


# Parsing functions

def parse_row_to_shape(row: dict[str, str]) -> Shape:
    """Convert a CSV row to Shape object."""
    return Shape(
        id=row["shape_id"],
        lat=float(row["shape_pt_lat"]),
        lon=float(row["shape_pt_lon"]),
        sequence=int(row["shape_pt_sequence"]),
        dist_traveled=float(row["shape_dist_traveled"])
    )


def add_shape_to_lists(shape_lists: dict[str, ShapeLinkedList], shape: Shape) -> dict[str, ShapeLinkedList]:
    """Reducer function - groups shapes by id into linked lists."""
    if shape.id not in shape_lists:
        shape_lists[shape.id] = ShapeLinkedList(shape_id=shape.id)
    shape_lists[shape.id].add(shape)
    return shape_lists


def parse_shapes_file(filename: str) -> list[ShapeLinkedList]:
    """
    Parse shapes.txt into list of ShapeLinkedLists.
    Uses map, filter, reduce - traverses file only once.
    """
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)

        # map -> filter -> reduce
        shapes = map(parse_row_to_shape, reader)
        valid_shapes = filter(lambda s: s.id != "", shapes)
        shape_dict = reduce(add_shape_to_lists, valid_shapes, {})

        return list(shape_dict.values())


# Distance calculation (recursive)

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two lat/lon points in meters."""
    R = 6371000  # earth radius in meters

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c


def node_distance(n: Node) -> float:
    """
    Calculate total distance along linked list using recursion.

    Signature: Node -> float
    Purpose: Sum distances between consecutive shape points

    Example:
        n0 = Node(Shape("1", 49.0, -123.0, 1, 0.0), None)
        n1 = Node(Shape("1", 49.001, -123.0, 2, 100.0), n0)
        node_distance(n0) -> 0.0
        node_distance(n1) -> ~111.0

    Template:
        if n.next == None:  # base case
            return ...
        else:               # recursive step
            return ... + node_distance(n.next)

    Base case: n.next is None -> return 0
    Recursive step: distance to next + node_distance(n.next)
    """
    # base case
    if n.next == None:
        return 0.0
    else:
        # recursive step
        current_shape = n.data
        next_shape = n.next.data

        dist_to_next = haversine_distance(
            current_shape.lat, current_shape.lon,
            next_shape.lat, next_shape.lon
        )
        return dist_to_next + node_distance(n.next)


def calculate_shape_distance(shape_list: ShapeLinkedList) -> float:
    """Wrapper to calculate distance for a ShapeLinkedList."""
    if shape_list.head is None:
        return 0.0
    return node_distance(shape_list.head)


# Route analysis functions

def get_longest_route(shape_lists: list[ShapeLinkedList]) -> Optional[ShapeLinkedList]:
    """Find shape with longest distance using map + reduce."""
    if not shape_lists:
        return None

    distances = map(lambda sl: (sl, calculate_shape_distance(sl)), shape_lists)

    def pick_max(acc, curr):
        return acc if acc[1] >= curr[1] else curr

    result = reduce(pick_max, distances)
    return result[0]


def get_shortest_route(shape_lists: list[ShapeLinkedList]) -> Optional[ShapeLinkedList]:
    """Find shape with shortest distance using filter + map + reduce."""
    if not shape_lists:
        return None

    non_empty = list(filter(lambda sl: len(sl) > 0, shape_lists))
    if not non_empty:
        return None

    distances = map(lambda sl: (sl, calculate_shape_distance(sl)), non_empty)

    def pick_min(acc, curr):
        return acc if acc[1] <= curr[1] else curr

    result = reduce(pick_min, distances)
    return result[0]


def get_average_route_length(shape_lists: list[ShapeLinkedList]) -> float:
    """Calculate average distance using map + reduce."""
    if not shape_lists:
        return 0.0

    non_empty = list(filter(lambda sl: len(sl) > 0, shape_lists))
    if not non_empty:
        return 0.0

    distances = list(map(calculate_shape_distance, non_empty))
    total = reduce(lambda acc, d: acc + d, distances, 0.0)

    return total / len(distances)


def get_routes_longer_than(shape_lists: list[ShapeLinkedList], min_dist: float) -> list[ShapeLinkedList]:
    """Filter to shapes longer than min_dist."""
    with_dist = map(lambda sl: (sl, calculate_shape_distance(sl)), shape_lists)
    filtered = filter(lambda p: p[1] > min_dist, with_dist)
    return [p[0] for p in filtered]


if __name__ == "__main__":
    print("Parsing shapes.txt...")
    shape_lists = parse_shapes_file("shapes.txt")

    print(f"\nFound {len(shape_lists)} unique shapes:")

    for sl in shape_lists:
        dist = calculate_shape_distance(sl)
        print(f"  Shape {sl.shape_id}: {len(sl)} points, {dist:.2f} meters")

        for i, shape in enumerate(sl):
            if i < 3:
                print(f"    Point {shape.sequence}: ({shape.lat}, {shape.lon})")
            elif i == 3:
                print(f"    ... ({len(sl) - 3} more points)")
                break

    print("\n--- Route Analysis ---")

    longest = get_longest_route(shape_lists)
    if longest:
        print(f"Longest route: Shape {longest.shape_id} ({calculate_shape_distance(longest):.2f} meters)")

    shortest = get_shortest_route(shape_lists)
    if shortest:
        print(f"Shortest route: Shape {shortest.shape_id} ({calculate_shape_distance(shortest):.2f} meters)")

    avg = get_average_route_length(shape_lists)
    print(f"Average route length: {avg:.2f} meters")
