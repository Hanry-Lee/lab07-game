# Lab 10: Sorting and Complexity

## Individual Lab

### Comparable Shape Class
Implemented all comparison methods for the `Shape` class in `shape_sort.py`:
- `__eq__`: equality check
- `__lt__`: less than
- `__le__`: less than or equal
- `__gt__`: greater than
- `__ge__`: greater than or equal

Shapes are ordered by `shape_id` first, then by `shape_pt_sequence`.

### Selection Sort (HtDF)
Implemented three functions following the HtDF formula with signature, purpose, and examples:
- `min_index(los)`: finds index of minimum Shape in list
- `swap(los, i, j)`: swaps elements at indices i and j
- `selection_sort(los)`: sorts list using selection sort O(n^2)

### Performance Comparison
Timed Selection Sort vs Python's built-in sort at sizes 100, 1000, and 10000:

| Size   | Selection Sort | Built-in Sort | Ratio  |
|--------|----------------|---------------|--------|
| 100    | ~0.0003s       | ~0.00003s     | ~10x   |
| 1000   | ~0.03s         | ~0.0006s      | ~50x   |
| 10000  | ~3.5s          | ~0.007s       | ~500x  |

Selection Sort is O(n^2), Python's sorted() is O(n log n) using Timsort.

## Group Lab

*Note: I completed the group part solely.*

### Comparable Classes
Made the following classes comparable for sorting:

- **Sprite** (`sprite.py`): comparable by `size`
- **Character** (`character.py`): comparable by `count` (score)
- **Food** (`food.py`): comparable by `size`

### Sortable Collection
**FoodList** (`food.py`) supports multiple sorting methods:
- `sort()`: by natural order (size)
- `sort_by_size()`: by food size
- `sort_by_distance(point)`: by distance from a point
- `sort_by_x()`: by x position
- `sort_by_y()`: by y position

### UML Diagram
See `uml.png` for the class diagram showing all sortable classes with their comparison methods.

## Running the Code

```bash
# Run timing comparison
python shape_sort.py

# Run tests (48 tests)
python shape_sort_tests.py
```
