"""Tests for shape_sort.py"""
from cs110 import expect, summarize
from shape_sort import Shape, min_index, swap, selection_sort

# Test data
s1_1 = Shape("1", 49.0, -123.0, 1, 0.0)
s1_2 = Shape("1", 49.1, -123.1, 2, 100.0)
s1_3 = Shape("1", 49.2, -123.2, 3, 200.0)
s2_1 = Shape("2", 49.0, -123.0, 1, 0.0)
s2_2 = Shape("2", 49.1, -123.1, 2, 100.0)

# Shape comparison tests
print("Testing Shape comparison...")
expect(s1_1 == s1_1, True)
expect(s1_1 == Shape("1", 49.0, -123.0, 1, 0.0), True)
expect(s1_1 == s1_2, False)
expect(s1_1 == s2_1, False)

expect(s1_1 < s1_2, True)
expect(s1_2 < s1_1, False)
expect(s1_1 < s2_1, True)
expect(s2_1 < s1_1, False)
expect(s1_1 < s1_1, False)

expect(s1_1 <= s1_1, True)
expect(s1_1 <= s1_2, True)
expect(s1_2 <= s1_1, False)

expect(s1_2 > s1_1, True)
expect(s1_1 > s1_2, False)
expect(s1_1 > s1_1, False)

expect(s1_1 >= s1_1, True)
expect(s1_2 >= s1_1, True)
expect(s1_1 >= s1_2, False)

# min_index tests
print("Testing min_index...")
expect(min_index([s1_1]), 0)
expect(min_index([s1_1, s1_2]), 0)
expect(min_index([s1_2, s1_1]), 1)
expect(min_index([s1_2, s1_3, s1_1]), 2)
expect(min_index([s2_1, s1_1]), 1)
expect(min_index([s1_1, s2_1]), 0)

# swap tests
print("Testing swap...")
test_list = [s1_1, s1_2]
result = swap(test_list, 0, 1)
expect(result[0], s1_2)
expect(result[1], s1_1)

test_list2 = [s1_1, s1_2, s1_3]
swap(test_list2, 0, 2)
expect(test_list2[0], s1_3)
expect(test_list2[2], s1_1)

# selection_sort tests
print("Testing selection_sort...")
expect(selection_sort([]), [])
expect(selection_sort([s1_1]), [s1_1])

result = selection_sort([s1_1, s1_2])
expect(result[0], s1_1)
expect(result[1], s1_2)

result = selection_sort([s1_2, s1_1])
expect(result[0], s1_1)
expect(result[1], s1_2)

result = selection_sort([s1_3, s1_1, s1_2])
expect(result[0], s1_1)
expect(result[1], s1_2)
expect(result[2], s1_3)

result = selection_sort([s2_1, s1_2, s1_1, s2_2])
expect(result[0], s1_1)
expect(result[1], s1_2)
expect(result[2], s2_1)
expect(result[3], s2_2)

# verify original not mutated
original = [s1_2, s1_1]
sorted_list = selection_sort(original)
expect(original[0], s1_2)
expect(original[1], s1_1)

# verify matches built-in sort
print("Testing against built-in sort...")
test_shapes = [s2_2, s1_3, s2_1, s1_1, s1_2]
selection_result = selection_sort(test_shapes)
builtin_result = sorted(test_shapes)
for i in range(len(test_shapes)):
    expect(selection_result[i], builtin_result[i])

print()
summarize()
