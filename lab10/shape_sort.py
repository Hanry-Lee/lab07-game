"""Lab 10: Sorting and Complexity - Shape sorting with Selection Sort."""
from __future__ import annotations
from dataclasses import dataclass
from typing import List
import time
import csv
import random
from cs110 import expect


@dataclass
class Shape:
    """Shape point from GTFS shapes.txt. Comparable by shape_id then sequence."""
    shape_id: str
    shape_pt_lat: float
    shape_pt_lon: float
    shape_pt_sequence: int
    shape_dist_traveled: float

    def __eq__(self, other: object) -> bool:
        """Check if two Shapes are equal (same id and sequence)."""
        if not isinstance(other, Shape):
            return NotImplemented
        return (self.shape_id == other.shape_id and
                self.shape_pt_sequence == other.shape_pt_sequence)

    def __lt__(self, other: Shape) -> bool:
        """Compare by shape_id first, then by sequence."""
        if self.shape_id != other.shape_id:
            return self.shape_id < other.shape_id
        return self.shape_pt_sequence < other.shape_pt_sequence

    def __le__(self, other: Shape) -> bool:
        return self == other or self < other

    def __gt__(self, other: Shape) -> bool:
        return not self <= other

    def __ge__(self, other: Shape) -> bool:
        return self == other or self > other


def parse_row_to_shape(row: dict[str, str]) -> Shape:
    """Parse a CSV row into a Shape object."""
    return Shape(
        shape_id=row["shape_id"],
        shape_pt_lat=float(row["shape_pt_lat"]),
        shape_pt_lon=float(row["shape_pt_lon"]),
        shape_pt_sequence=int(row["shape_pt_sequence"]),
        shape_dist_traveled=float(row["shape_dist_traveled"])
    )


def parse_shapes_file(filename: str) -> List[Shape]:
    """Parse shapes.txt into a list of Shapes."""
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        return [parse_row_to_shape(row) for row in reader]


def min_index(los: List[Shape]) -> int:
    """
    Purpose: Find the index of the minimum Shape in the list.
    Assume: List is non-empty
    Examples:
        min_index([Shape("1",0,0,2,0), Shape("1",0,0,1,0)]) -> 1
        min_index([Shape("1",0,0,1,0), Shape("1",0,0,2,0)]) -> 0
    """
    minimum_index = 0
    for i in range(len(los)):
        if los[i] < los[minimum_index]:
            minimum_index = i
    return minimum_index


def swap(los: List[Shape], i: int, j: int) -> List[Shape]:
    """
    Purpose: Swap the values at indices i and j.
    Assume: List is non-empty, indices < len(list)
    Examples:
        swap([s1, s2], 0, 1) -> [s2, s1]
    """
    los[i], los[j] = los[j], los[i]
    return los


def selection_sort(los: List[Shape]) -> List[Shape]:
    """
    Purpose: Sort a list of Shapes using selection sort.
    Examples:
        selection_sort([]) -> []
        selection_sort([s1]) -> [s1]
        selection_sort([s2, s1]) -> [s1, s2]  where s1 < s2
    Complexity: O(n^2)
    """
    result = los.copy()
    for i in range(len(result)):
        min_i = i + min_index(result[i:])
        swap(result, i, min_i)
    return result


def generate_random_shapes(n: int) -> List[Shape]:
    """Generate n random Shape objects for testing."""
    shapes = []
    for i in range(n):
        shapes.append(Shape(
            shape_id=str(random.randint(1, n // 10 + 1)),
            shape_pt_lat=random.uniform(49.0, 50.0),
            shape_pt_lon=random.uniform(-124.0, -122.0),
            shape_pt_sequence=random.randint(1, 100),
            shape_dist_traveled=random.uniform(0, 1000)
        ))
    return shapes


def time_selection_sort(shapes: List[Shape]) -> float:
    """Time how long selection_sort takes. Returns seconds."""
    shapes_copy = shapes.copy()
    start = time.perf_counter()
    selection_sort(shapes_copy)
    end = time.perf_counter()
    return end - start


def time_builtin_sort(shapes: List[Shape]) -> float:
    """Time how long Python's built-in sort takes. Returns seconds."""
    shapes_copy = shapes.copy()
    start = time.perf_counter()
    sorted(shapes_copy)
    end = time.perf_counter()
    return end - start


def run_timing_comparison(sizes: List[int] = [100, 1000, 10000]) -> None:
    """Compare selection sort vs built-in sort at different sizes."""
    print("Timing: Selection Sort vs Built-in Sort")
    print(f"{'Size':<10} {'Selection':<15} {'Built-in':<15} {'Ratio':<10}")

    for size in sizes:
        shapes = generate_random_shapes(size)
        sel_time = time_selection_sort(shapes)
        builtin_time = time_builtin_sort(shapes)
        ratio = sel_time / builtin_time if builtin_time > 0 else float('inf')
        print(f"{size:<10} {sel_time:<15.4f} {builtin_time:<15.6f} {ratio:<10.1f}x")

    print("Selection Sort: O(n^2), Built-in: O(n log n)")


if __name__ == "__main__":
    print("Parsing shapes from ../lab09/shapes.txt...")
    try:
        shapes = parse_shapes_file("../lab09/shapes.txt")
        print(f"Loaded {len(shapes)} shapes.\n")

        print("First 5 shapes (unsorted):")
        for s in shapes[:5]:
            print(f"  Shape {s.shape_id}, seq={s.shape_pt_sequence}")

        sorted_shapes = selection_sort(shapes)
        print("\nFirst 5 shapes (sorted):")
        for s in sorted_shapes[:5]:
            print(f"  Shape {s.shape_id}, seq={s.shape_pt_sequence}")

    except FileNotFoundError:
        print("shapes.txt not found. Using generated data.\n")

    print("\n")
    run_timing_comparison([100, 1000, 10000])
